"""Completion criteria checked by code, never by the model's own claim (Buổi 3).

Each use case implements ``CompletionCriteria`` for its own definition of "done" (evidence
coverage for UC3, ``check_geo.py`` PASS for UC4, no open claims for UC5...). The harness only
needs ``check()``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from geo.harness.steps import StepLog


@dataclass(frozen=True)
class Check:
    name: str
    passed: bool
    detail: str = ""


@dataclass
class CompletionResult:
    done: bool
    checks: list[Check] = field(default_factory=list)

    @classmethod
    def of(cls, checks: list[Check]) -> CompletionResult:
        return cls(bool(checks) and all(c.passed for c in checks), checks)

    def summary(self) -> str:
        return " · ".join(f"{'✓' if c.passed else '✗'} {c.name}" for c in self.checks)


class CompletionCriteria(Protocol):
    def check(self, steps: StepLog, answer: str | None) -> CompletionResult: ...
