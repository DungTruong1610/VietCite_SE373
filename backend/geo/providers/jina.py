"""Jina AI client: embeddings, rerank, Reader (page → Markdown) and Search.

- One ``httpx.Client`` with timeout; retries with exponential backoff on 429 and 5xx.
- ``tokens_used`` accumulates the token usage Jina reports, for the cost dashboard.
- The API key goes in the Authorization header only; it is never logged or put in errors.
- ``MockJina`` is a deterministic offline stand-in for tests and CI.

Fallbacks for Reader/Search (trafilatura, ddgs) and snapshot caching come with Phase 2.
"""

from __future__ import annotations

import hashlib
import math
import time
from dataclasses import dataclass, field
from typing import Any, Protocol
from urllib.parse import quote

import httpx

EMBED_URL = "https://api.jina.ai/v1/embeddings"
RERANK_URL = "https://api.jina.ai/v1/rerank"
READER_URL = "https://r.jina.ai/"
SEARCH_URL = "https://s.jina.ai/"
RETRY_STATUS = {429, 500, 502, 503, 504}


class ProviderError(RuntimeError):
    def __init__(
        self, provider: str, message: str, status: int | None = None, retryable: bool = False
    ) -> None:
        super().__init__(f"{provider}: {message}")
        self.provider, self.status, self.retryable = provider, status, retryable


@dataclass(frozen=True)
class RerankHit:
    index: int
    score: float
    text: str


@dataclass(frozen=True)
class Page:
    url: str
    title: str
    content: str


@dataclass(frozen=True)
class SearchHit:
    url: str
    title: str
    snippet: str
    content: str = ""


class JinaApi(Protocol):
    tokens_used: int

    def embed(self, texts: list[str], task: str = "retrieval.passage") -> list[list[float]]: ...
    def rerank(self, query: str, documents: list[str], top_n: int = 5) -> list[RerankHit]: ...
    def read(self, url: str) -> Page: ...
    def search(self, query: str, limit: int = 5) -> list[SearchHit]: ...


@dataclass
class JinaClient:
    api_key: str = field(repr=False)  # never printed in reprs, tracebacks or test failures
    embedding_model: str = "jina-embeddings-v3"
    reranker_model: str = "jina-reranker-v2-base-multilingual"
    timeout_s: float = 30.0
    max_retries: int = 3
    backoff_s: float = 1.0
    http: httpx.Client | None = None
    tokens_used: int = 0
    _owned: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if self.http is None:
            self.http = httpx.Client(timeout=self.timeout_s)
            self._owned = True

    def close(self) -> None:
        if self._owned and self.http is not None:
            self.http.close()

    # ------------------------------------------------------------ transport
    def _request(
        self,
        method: str,
        url: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        assert self.http is not None
        all_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            **(headers or {}),
        }
        for attempt in range(self.max_retries + 1):
            try:
                resp = self.http.request(method, url, json=json, headers=all_headers)
            except httpx.TimeoutException as exc:
                if attempt < self.max_retries:
                    time.sleep(self.backoff_s * 2**attempt)
                    continue
                raise ProviderError("jina", f"timeout calling {_endpoint(url)}", retryable=True) from exc
            except httpx.HTTPError as exc:
                raise ProviderError(
                    "jina", f"network error calling {_endpoint(url)}: {type(exc).__name__}"
                ) from exc
            if resp.status_code in RETRY_STATUS and attempt < self.max_retries:
                time.sleep(self.backoff_s * 2**attempt)
                continue
            if resp.status_code >= 400:
                raise ProviderError(
                    "jina",
                    f"HTTP {resp.status_code} from {_endpoint(url)}: {_detail(resp)}",
                    status=resp.status_code,
                    retryable=resp.status_code in RETRY_STATUS,
                )
            return resp.json()
        raise ProviderError("jina", "retries exhausted", retryable=True)  # pragma: no cover

    # ------------------------------------------------------------ API
    def embed(self, texts: list[str], task: str = "retrieval.passage") -> list[list[float]]:
        """``task``: retrieval.passage when indexing, retrieval.query when searching."""
        data = self._request(
            "POST", EMBED_URL, json={"model": self.embedding_model, "task": task, "input": texts}
        )
        self.tokens_used += int((data.get("usage") or {}).get("total_tokens") or 0)
        rows = sorted(data["data"], key=lambda r: r["index"])
        return [r["embedding"] for r in rows]

    def rerank(self, query: str, documents: list[str], top_n: int = 5) -> list[RerankHit]:
        data = self._request(
            "POST",
            RERANK_URL,
            json={"model": self.reranker_model, "query": query, "documents": documents, "top_n": top_n},
        )
        self.tokens_used += int((data.get("usage") or {}).get("total_tokens") or 0)
        return [
            RerankHit(int(r["index"]), float(r["relevance_score"]), _document_text(r, documents))
            for r in data["results"]
        ]

    def read(self, url: str) -> Page:
        data = self._request("GET", READER_URL + url)["data"]
        self.tokens_used += int((data.get("usage") or {}).get("tokens") or 0)
        return Page(data.get("url") or url, data.get("title") or "", data.get("content") or "")

    def search(self, query: str, limit: int = 5) -> list[SearchHit]:
        data = self._request(
            "GET", SEARCH_URL + "?q=" + quote(query), headers={"X-Respond-With": "no-content"}
        )
        hits = []
        for row in (data.get("data") or [])[:limit]:
            self.tokens_used += int((row.get("usage") or {}).get("tokens") or 0)
            hits.append(
                SearchHit(
                    row.get("url", ""),
                    row.get("title", ""),
                    row.get("description", ""),
                    row.get("content", ""),
                )
            )
        return hits


def _document_text(row: dict[str, Any], documents: list[str]) -> str:
    """Rerank rows carry the document as a string or as ``{"text": ...}`` depending on the API version."""
    doc = row.get("document")
    if isinstance(doc, str) and doc:
        return doc
    if isinstance(doc, dict) and doc.get("text"):
        return str(doc["text"])
    return documents[int(row["index"])]


def _endpoint(url: str) -> str:
    return url.split("?")[0][:60]


def _detail(resp: httpx.Response) -> str:
    try:
        body = resp.json()
        return str(body.get("detail") or body.get("message") or body)[:200]
    except ValueError:
        return resp.text[:200]


class MockJina:
    """Deterministic offline stand-in: hashed bag-of-words vectors, overlap-based rerank."""

    DIM = 64

    def __init__(self, pages: dict[str, Page] | None = None) -> None:
        self.pages = pages or {}
        self.tokens_used = 0

    def _vector(self, text: str) -> list[float]:
        vec = [0.0] * self.DIM
        for word in text.lower().split():
            vec[int(hashlib.md5(word.encode()).hexdigest(), 16) % self.DIM] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def embed(self, texts: list[str], task: str = "retrieval.passage") -> list[list[float]]:
        self.tokens_used += sum(len(t.split()) for t in texts)
        return [self._vector(t) for t in texts]

    def rerank(self, query: str, documents: list[str], top_n: int = 5) -> list[RerankHit]:
        q = set(query.lower().split())
        scored = [
            RerankHit(i, len(q & set(d.lower().split())) / (len(q) or 1), d) for i, d in enumerate(documents)
        ]
        return sorted(scored, key=lambda h: (-h.score, h.index))[:top_n]

    def read(self, url: str) -> Page:
        if url not in self.pages:
            raise ProviderError("jina-mock", f"no fixture page for {url}", status=404)
        return self.pages[url]

    def search(self, query: str, limit: int = 5) -> list[SearchHit]:
        hits = [
            SearchHit(p.url, p.title, p.content[:160])
            for p in self.pages.values()
            if set(query.lower().split()) & set(p.content.lower().split())
        ]
        return hits[:limit]
