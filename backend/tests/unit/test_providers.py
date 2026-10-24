"""Jina client against a fake transport; Gemini grounding parser on plain dicts."""

from __future__ import annotations

import json

import httpx
import pytest

from geo.providers.gemini_probe import parse_response
from geo.providers.jina import JinaClient, MockJina, Page, ProviderError

KEY = "test-key-not-real"


def _client(handler) -> JinaClient:
    return JinaClient(api_key=KEY, http=httpx.Client(transport=httpx.MockTransport(handler)), backoff_s=0)


def test_embed_sends_task_and_counts_tokens():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(request.content)
        seen["auth"] = request.headers["Authorization"]
        return httpx.Response(
            200,
            json={
                "data": [{"index": 1, "embedding": [0.2]}, {"index": 0, "embedding": [0.1]}],
                "usage": {"total_tokens": 7},
            },
        )

    client = _client(handler)
    vectors = client.embed(["a", "b"], task="retrieval.query")
    assert vectors == [[0.1], [0.2]]  # sorted by index
    assert seen["body"]["task"] == "retrieval.query" and seen["auth"] == f"Bearer {KEY}"
    assert client.tokens_used == 7


def test_retries_on_429_then_succeeds():
    attempts = []

    def handler(request: httpx.Request) -> httpx.Response:
        attempts.append(1)
        if len(attempts) < 3:
            return httpx.Response(429, json={"detail": "rate limited"})
        return httpx.Response(200, json={"results": [{"index": 0, "relevance_score": 0.9}], "usage": {}})

    hits = _client(handler).rerank("q", ["doc"])
    assert len(attempts) == 3 and hits[0].text == "doc" and hits[0].score == 0.9


def test_error_message_never_contains_the_key():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"detail": "invalid key"})

    with pytest.raises(ProviderError) as exc:
        _client(handler).read("https://example.com")
    assert exc.value.status == 401 and KEY not in str(exc.value)


def test_reader_and_search_parse_payloads():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "r.jina.ai":
            return httpx.Response(
                200,
                json={
                    "data": {"title": "T", "url": "https://x.vn", "content": "# Hi", "usage": {"tokens": 3}}
                },
            )
        assert request.headers["X-Respond-With"] == "no-content"
        return httpx.Response(200, json={"data": [{"title": "A", "url": "https://a.vn", "description": "d"}]})

    client = _client(handler)
    assert client.read("https://x.vn") == Page("https://x.vn", "T", "# Hi")
    assert client.search("phần mềm bán hàng")[0].url == "https://a.vn"


def test_mock_jina_is_deterministic():
    mock = MockJina({"u": Page("u", "Bảng giá", "gói cơ bản gói nâng cao")})
    assert mock.embed(["a b"]) == mock.embed(["a b"])
    assert mock.rerank("gói nâng cao", ["khác hẳn", "gói nâng cao"])[0].index == 1
    assert mock.search("gói")[0].url == "u"


def test_gemini_grounding_metadata_parsed():
    response = {
        "candidates": [
            {
                "content": {"parts": [{"text": "KiotViet và Sapo là hai lựa chọn phổ biến."}]},
                "grounding_metadata": {
                    "grounding_chunks": [
                        {"web": {"uri": "https://kiotviet.vn/x", "title": "kiotviet.vn"}},
                        {"web": {"uri": "https://sapo.vn/y", "title": "sapo.vn"}},
                    ],
                    "grounding_supports": [
                        {"segment": {"text": "KiotViet và Sapo"}, "grounding_chunk_indices": [0, 1]}
                    ],
                    "web_search_queries": ["phần mềm bán hàng"],
                },
            }
        ]
    }
    result = parse_response("q", "gemini-x", response)
    assert result.mentions(["Sapo"]) and not result.mentions(["Tallyo"])
    assert result.cites_domain("kiotviet.vn") and result.supports[0].source_indices == (0, 1)
    assert result.search_queries == ["phần mềm bán hàng"]
    assert parse_response("q", "m", {"candidates": []}).text == ""


def test_rerank_accepts_document_as_string_or_object():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "results": [
                    {"index": 1, "relevance_score": 0.8, "document": "b as string"},
                    {"index": 0, "relevance_score": 0.2, "document": {"text": "a as object"}},
                ]
            },
        )

    hits = _client(handler).rerank("q", ["a", "b"], top_n=2)
    assert [h.text for h in hits] == ["b as string", "a as object"]
