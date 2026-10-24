"""Calls real APIs and costs a little money. Run explicitly: ``uv run pytest -m live``.

Each test skips when its key is missing, so the suite is safe to run on any machine.
"""

from __future__ import annotations

import pytest

from geo.config import get_settings

pytestmark = pytest.mark.live
QUESTION = (
    "Một shop bán 2.400.000đ mỗi ngày. 30 ngày thì doanh thu bao nhiêu, và 1,5% của số đó là bao nhiêu?"
)


@pytest.fixture(scope="module")
def s():
    get_settings.cache_clear()
    return get_settings()


def test_deepseek_hello_agent_reaches_goal(s):
    if not s.features["deepseek"]:
        pytest.skip("DEEPSEEK_API_KEY not set")
    from geo.agents.hello import run_hello

    r = run_hello(QUESTION, mode="live", use_cache=False)
    assert r.stop_reason == "GOAL", r.detail
    assert r.usage["tool_calls"] >= 1 and r.usage["cost_usd"] > 0


def test_jina_embed_rerank_reader(s):
    if not s.features["jina"]:
        pytest.skip("JINA_API_KEY not set")
    from geo.providers.jina import JinaClient

    jina = JinaClient(s.jina_api_key or "", s.jina_embedding_model, s.jina_reranker_model)
    try:
        vectors = jina.embed(["phần mềm bán hàng", "hoá đơn điện tử"], task="retrieval.passage")
        assert len(vectors) == 2 and len(vectors[0]) > 100
        hits = jina.rerank(
            "xuất hoá đơn điện tử", ["giá cà phê Đà Lạt", "phần mềm xuất hoá đơn điện tử"], top_n=2
        )
        assert hits[0].index == 1
        page = jina.read("https://example.com")
        assert page.title == "Example Domain" and page.content
        assert jina.tokens_used > 0
    finally:
        jina.close()


def test_gemini_grounded_probe(s):
    if not s.features["gemini"]:
        pytest.skip("GEMINI_API_KEY not set")
    from geo.providers.gemini_probe import GeminiProbe

    r = GeminiProbe(s.gemini_api_key or "", s.gemini_model).probe(
        "Phần mềm quản lý bán hàng phổ biến ở Việt Nam?"
    )
    assert r.text and r.sources
