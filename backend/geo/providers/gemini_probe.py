"""Gemini with Google Search grounding: a real AI answer engine with its cited web sources (UC7).

``probe(question)`` asks Gemini with the ``google_search`` tool and returns the answer text plus
the sources it grounded on (``groundingMetadata``). Parsing is a pure function so it can be tested
without the network.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class GroundingSource:
    uri: str
    title: str


@dataclass(frozen=True)
class GroundingSupport:
    text: str
    source_indices: tuple[int, ...]


@dataclass
class ProbeResult:
    question: str
    model: str
    text: str
    sources: list[GroundingSource] = field(default_factory=list)
    supports: list[GroundingSupport] = field(default_factory=list)
    search_queries: list[str] = field(default_factory=list)

    def mentions(self, aliases: list[str]) -> bool:
        lowered = self.text.lower()
        return any(a.lower() in lowered for a in aliases)

    def cites_domain(self, domain: str) -> bool:
        d = domain.lower()
        return any(d in s.uri.lower() or d in s.title.lower() for s in self.sources)


def _get(obj: Any, name: str, default: Any = None) -> Any:
    """Read a field from an SDK object or a plain dict (tests use dicts)."""
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)


def parse_response(question: str, model: str, response: Any) -> ProbeResult:
    candidates = _get(response, "candidates") or []
    if not candidates:
        return ProbeResult(question, model, "")
    cand = candidates[0]
    parts = _get(_get(cand, "content"), "parts") or []
    text = "".join(_get(p, "text") or "" for p in parts)
    meta = _get(cand, "grounding_metadata")
    sources, supports, queries = [], [], []
    if meta is not None:
        for chunk in _get(meta, "grounding_chunks") or []:
            web = _get(chunk, "web")
            if web is not None:
                sources.append(GroundingSource(_get(web, "uri") or "", _get(web, "title") or ""))
        for sup in _get(meta, "grounding_supports") or []:
            segment = _get(sup, "segment")
            supports.append(
                GroundingSupport(
                    _get(segment, "text") or "", tuple(_get(sup, "grounding_chunk_indices") or [])
                )
            )
        queries = list(_get(meta, "web_search_queries") or [])
    return ProbeResult(question, model, text, sources, supports, queries)


class GeminiProbe:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash") -> None:
        from google import genai

        self.model = model
        self._client = genai.Client(api_key=api_key)

    def probe(self, question: str) -> ProbeResult:
        from google.genai import types

        config = types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())], temperature=0
        )
        response = self._client.models.generate_content(model=self.model, contents=question, config=config)
        return parse_response(question, self.model, response)
