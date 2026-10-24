"""Count model calls, tokens and cost for one run (ported from Buổi 3, extended for Buổi 7).

Two different caches are counted separately, because they are different things:
- **prompt cache** (provider side): input tokens the provider reused from a cached prefix. Still in
  the context window, only cheaper. DeepSeek reports them as ``prompt_cache_hit_tokens``.
- **response cache** (our SQLite cache): the whole answer was replayed locally, no API call, cost 0.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.outputs import LLMResult

from geo.config import Price

CHARS_PER_TOKEN = 4  # rough estimate for the mock model only


@dataclass
class CallRecord:
    role: str
    model: str
    tokens_in: int
    tokens_out: int
    cached_tokens: int
    cost_usd: float
    response_cache_hit: bool


@dataclass
class Usage:
    """Shared counter for one run."""

    model_calls: int = 0
    tool_calls: int = 0
    tokens_in: int = 0
    tokens_out: int = 0
    cached_tokens: int = 0
    response_cache_hits: int = 0
    cost_usd: float = 0.0
    calls: list[CallRecord] = field(default_factory=list)
    started: float = field(default_factory=time.perf_counter)

    @property
    def tokens(self) -> int:
        return self.tokens_in + self.tokens_out

    @property
    def elapsed(self) -> float:
        return time.perf_counter() - self.started

    @property
    def cache_hit_rate(self) -> float:
        """Share of input tokens served from the provider's prompt cache."""
        return self.cached_tokens / self.tokens_in if self.tokens_in else 0.0

    def summary(self) -> dict[str, Any]:
        return {
            "model_calls": self.model_calls,
            "tool_calls": self.tool_calls,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "cached_tokens": self.cached_tokens,
            "cache_hit_rate": round(self.cache_hit_rate, 4),
            "response_cache_hits": self.response_cache_hits,
            "cost_usd": round(self.cost_usd, 6),
            "elapsed_s": round(self.elapsed, 2),
        }


def estimate_tokens(messages: list[BaseMessage]) -> int:
    chars = 0
    for m in messages:
        chars += len(str(m.content))
        chars += len(json.dumps(getattr(m, "tool_calls", None) or [], ensure_ascii=False))
    return max(1, chars // CHARS_PER_TOKEN)


def cost_of(price: Price, tokens_in: int, tokens_out: int, cached: int) -> float:
    uncached = max(0, tokens_in - cached)
    return (uncached * price.input + cached * price.cached_input + tokens_out * price.output) / 1_000_000


def cached_tokens_from(message: Any) -> int:
    """Prompt-cache hits from either the LangChain standard field or DeepSeek's raw usage."""
    meta = getattr(message, "usage_metadata", None) or {}
    details = meta.get("input_token_details") or {}
    if details.get("cache_read"):
        return int(details["cache_read"])
    raw = (getattr(message, "response_metadata", None) or {}).get("token_usage") or {}
    return int(raw.get("prompt_cache_hit_tokens") or 0)


class UsageCallback(BaseCallbackHandler):
    """Updates ``Usage`` after each model call."""

    def __init__(self, usage: Usage, price: Price, model: str, role: str = "agent") -> None:
        self.usage, self.price, self.model, self.role = usage, price, model, role
        self._pending_in = 0

    def on_chat_model_start(
        self, serialized: dict[str, Any], messages: list[list[BaseMessage]], **kwargs: Any
    ) -> None:
        self._pending_in = sum(estimate_tokens(batch) for batch in messages)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        gen = response.generations[0][0]
        msg = getattr(gen, "message", None)
        from_cache = bool((getattr(msg, "response_metadata", None) or {}).get("response_cache_hit"))
        meta = getattr(msg, "usage_metadata", None) or {}
        t_in = int(meta.get("input_tokens") or self._pending_in)
        t_out = int(
            meta.get("output_tokens") or max(1, len(str(getattr(msg, "content", ""))) // CHARS_PER_TOKEN)
        )
        cached = cached_tokens_from(msg)
        cost = 0.0 if from_cache else cost_of(self.price, t_in, t_out, cached)
        u = self.usage
        u.model_calls += 1
        if from_cache:
            u.response_cache_hits += 1
        else:
            u.tokens_in += t_in
            u.tokens_out += t_out
            u.cached_tokens += cached
            u.cost_usd += cost
        u.calls.append(CallRecord(self.role, self.model, t_in, t_out, cached, cost, from_cache))
