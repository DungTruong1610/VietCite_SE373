"""Hand-off packet for a human or another agent (Buổi 3).

"A good hand-off can be answered in 30 seconds": why it stopped, what was tried (including side
effects that already happened), the current state, and ONE concrete question.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from geo.harness.steps import StepLog
from geo.harness.types import StopReason

QUESTIONS: dict[StopReason, str] = {
    StopReason.BUDGET: "Budget exhausted before the goal was reached. Raise the budget or narrow the task?",
    StopReason.LOOP: "The agent repeated the same failing action. Retry later, or change the input?",
    StopReason.STALL: "No progress for several steps. Which constraint should be relaxed?",
    StopReason.NEEDS_HUMAN: "This action needs a human decision. Approve or reject?",
    StopReason.UNGROUNDED: (
        "The answer contained facts with no source and was blocked. "
        "Re-run with tighter instructions, or answer manually?"
    ),
    StopReason.UNVERIFIED: "The agent said it was done but the completion checks failed. Accept or re-run?",
    StopReason.ERROR: "The run failed with an error. Check the trace and re-run?",
}


class HandoffPacket(BaseModel):
    stop_reason: StopReason
    detail: str
    tried: list[str] = Field(default_factory=list)
    state: dict[str, Any] = Field(default_factory=dict)
    question: str

    def render(self) -> str:
        tried = "\n".join(f"  - {t}" for t in self.tried) or "  (no tool call)"
        state = ", ".join(f"{k}={v}" for k, v in self.state.items())
        return (
            f"[HANDOFF] {self.stop_reason.value}: {self.detail}\n"
            f"Tried:\n{tried}\nState: {state}\nQuestion: {self.question}"
        )


def build_handoff(
    reason: StopReason, detail: str, steps: StepLog, state: dict[str, Any], question: str | None = None
) -> HandoffPacket:
    side_effects = [s.short() for s in steps.steps if s.obs.get("side_effect")]
    return HandoffPacket(
        stop_reason=reason,
        detail=detail,
        tried=[s.short() for s in steps.steps],
        state={**state, "side_effects": side_effects or "none"},
        question=question or QUESTIONS.get(reason, "Review the result before using it."),
    )
