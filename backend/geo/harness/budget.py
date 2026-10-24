"""Loop budget: model calls · tokens · seconds · money (ported from Buổi 3).

Checked LAST in the checklist: if it ran first, every failure would be reported as "out of
budget" and the real cause would be lost.
"""

from __future__ import annotations

from dataclasses import dataclass

from geo.llm.usage import Usage


@dataclass(frozen=True)
class BudgetLimits:
    max_model_calls: int = 12
    max_tokens: int = 60_000
    max_seconds: float = 120.0
    max_cost_usd: float = 0.05


class Budget:
    def __init__(self, limits: BudgetLimits, usage: Usage) -> None:
        self.limits, self.usage = limits, usage

    def check(self) -> str | None:
        u, lim = self.usage, self.limits
        if u.model_calls >= lim.max_model_calls:
            return f"model called {u.model_calls}/{lim.max_model_calls} times"
        if u.tokens >= lim.max_tokens:
            return f"used {u.tokens:,} tokens / limit {lim.max_tokens:,}"
        if u.elapsed >= lim.max_seconds:
            return f"ran {u.elapsed:.1f}s / limit {lim.max_seconds:.0f}s"
        if u.cost_usd >= lim.max_cost_usd:
            return f"cost ${u.cost_usd:.4f} / limit ${lim.max_cost_usd:.2f}"
        return None
