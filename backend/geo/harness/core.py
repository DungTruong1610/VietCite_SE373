"""Harness: the code around the model (generalised from Buổi 3).

Independent of LangChain, so a ReAct agent (middleware), a planner graph or a plain workflow node
share the same control layer. Checklist order (Buổi 3):

    0  review()      BEFORE a tool runs      · schema + permission        → needs human / denied
    1  checkpoint()  after an observation    · completion criteria        → goal
    2                                        · repeated (tool, args)      → loop
    3                                        · progress not moving        → stall
    4                                        · steps/tokens/time/money    → budget (checked LAST)
    +  finalize()    model stops calling tools · grounding + completion   → goal / ungrounded / unverified
"""

from __future__ import annotations

import json
from collections.abc import Callable, Hashable
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from geo.harness.budget import Budget, BudgetLimits
from geo.harness.completion import CompletionCriteria, CompletionResult
from geo.harness.contract import enforce_contract, parse_observation
from geo.harness.grounding import GroundingReport, check_numbers
from geo.harness.handoff import HandoffPacket, build_handoff
from geo.harness.loop_detector import LoopDetector
from geo.harness.permission import GateDecision, PermissionGate, Verdict
from geo.harness.steps import Step, StepLog
from geo.harness.types import StopReason
from geo.llm.usage import Usage
from geo.tools.registry import ToolRegistry
from geo.tracing.trace import Tracer, fmt_call


class ApprovalMode(StrEnum):
    AUTO = "auto"  # approve automatically (tests, full runs)
    DENY = "deny"  # reject → stop NEEDS_HUMAN with a hand-off
    ASK = "ask"  # pause the graph with interrupt() and wait for a person


@dataclass(frozen=True)
class HarnessConfig:
    enabled: bool = True  # False = baseline without harness, for A/B comparisons
    limits: BudgetLimits = field(default_factory=BudgetLimits)
    approval: ApprovalMode = ApprovalMode.DENY
    window: int = 6
    repeat_k: int = 2
    stall_n: int = 5
    allowed_retries: int = 1


@dataclass
class StopEvent:
    reason: StopReason
    detail: str
    answer: str
    handoff: HandoffPacket | None = None
    completion: CompletionResult | None = None
    grounding: GroundingReport | None = None


def default_progress(steps: StepLog) -> Hashable:
    """Progress = number of distinct successful observations."""
    return len({json.dumps(s.obs, sort_keys=True, ensure_ascii=False) for s in steps.steps if s.ok})


class Harness:
    """One harness per run of one agent."""

    def __init__(
        self,
        agent: str,
        registry: ToolRegistry,
        gate: PermissionGate,
        usage: Usage,
        tracer: Tracer,
        config: HarnessConfig | None = None,
        completion: CompletionCriteria | None = None,
        request_text: str = "",
        progress: Callable[[StepLog], Hashable] = default_progress,
    ) -> None:
        self.agent, self.registry, self.gate = agent, registry, gate
        self.usage, self.tracer = usage, tracer
        self.config = config or HarnessConfig()
        self.completion, self.request_text, self.progress = completion, request_text, progress
        self.steps = StepLog()
        self.detector = LoopDetector(
            self.config.window,
            self.config.repeat_k,
            stall_n=self.config.stall_n,
            allowed_retries=self.config.allowed_retries,
            polling_tools=registry.polling_tools,
            write_tools=registry.write_tools,
        )
        self.budget = Budget(self.config.limits, usage)
        self.stop: StopEvent | None = None
        self._checked = 0

    # ------------------------------------------------------------ 0 · before a tool runs
    def review(self, tool: str, args: dict[str, Any]) -> GateDecision:
        invalid = self.registry.validate_call(tool, args)
        if invalid:
            return GateDecision(Verdict.DENY, invalid, reason=invalid.get("error", ""))
        if not self.config.enabled:
            return GateDecision(Verdict.ALLOW)
        decision = self.gate.gate(self.agent, tool, args)
        if decision.verdict is Verdict.ASK and decision.approval_key:
            if self.config.approval is ApprovalMode.AUTO:
                self.resolve(decision.approval_key, True, tool)
                return GateDecision(Verdict.ALLOW, approval_key=decision.approval_key)
            if self.config.approval is ApprovalMode.DENY:
                self.resolve(decision.approval_key, False, tool)
        return decision

    def resolve(self, key: str, approved: bool, tool: str) -> None:
        self.gate.record(key, approved)
        self.tracer.add(
            "approval", f"{'APPROVED' if approved else 'REJECTED'} · {tool}", approved=approved, key=key
        )
        if not approved:
            self._halt(StopReason.NEEDS_HUMAN, f"human rejected '{tool}'")

    def run_tool(
        self, call_id: str, tool: str, args: dict[str, Any], executor: Callable[[], Any] | None = None
    ) -> dict[str, Any]:
        """review → execute → normalise → record. ``executor`` lets the framework run the tool."""
        decision = self.review(tool, args)
        if decision.verdict is Verdict.ALLOW:
            raw = executor() if executor else self.registry.execute(tool, args)
            obs = enforce_contract(raw) if self.config.enabled else parse_observation(raw)
        else:
            obs = decision.observation or {"status": "denied", "error": "not_allowed"}
            self.tracer.add("gate", f"blocked {fmt_call(tool, args)} · {obs.get('error')}", **obs)
        self.steps.add(Step(call_id, tool, args, obs))
        self.usage.tool_calls += 1
        self.tracer.add("tool", _compact(obs), status=obs.get("status"), tool=tool, obs=obs)
        return obs

    # ------------------------------------------------------------ 1–4 · after an observation
    def checkpoint(self) -> StopEvent | None:
        if self.stop or not self.config.enabled:
            return self.stop
        if self.completion:
            res = self.completion.check(self.steps, None)
            if res.done:
                return self._halt(StopReason.GOAL, res.summary(), completion=res)
        new = self.steps.steps[self._checked :]
        self._checked = len(self.steps)
        for s in new:
            alarm = self.detector.check_action(s.tool, s.args, s.obs)
            if alarm:
                return self._halt(StopReason.LOOP, alarm)
        if new:
            alarm = self.detector.check_progress(self.progress(self.steps))
            if alarm:
                return self._halt(StopReason.STALL, alarm)
        alarm = self.budget.check()
        if alarm:
            return self._halt(StopReason.BUDGET, alarm)
        return None

    # ------------------------------------------------------------ the model stopped calling tools
    def finalize(self, answer: str) -> StopEvent:
        if self.stop:
            return self.stop
        if not self.config.enabled:
            return self._halt(StopReason.MODEL_STOPPED, "baseline trusts the model's answer", answer=answer)
        grounding = check_numbers(answer, [self.request_text, self.steps.observations_text()])
        res = self.completion.check(self.steps, answer) if self.completion else None
        if not grounding.ok:
            return self._halt(
                StopReason.UNGROUNDED,
                f"{len(grounding.ungrounded)} number(s) without source: {grounding.ungrounded}",
                completion=res,
                grounding=grounding,
            )
        if res is not None and not res.done:
            return self._halt(
                StopReason.UNVERIFIED,
                "completion checks failed: " + res.summary(),
                completion=res,
                grounding=grounding,
            )
        detail = res.summary() if res else "answer grounded"
        return self._halt(StopReason.GOAL, detail, answer=answer, completion=res, grounding=grounding)

    def fail(self, reason: StopReason, detail: str) -> StopEvent:
        return self.stop or self._halt(reason, detail)

    # ------------------------------------------------------------ internal
    def _halt(self, reason: StopReason, detail: str, answer: str | None = None, **extra: Any) -> StopEvent:
        handoff = None
        if reason is not StopReason.GOAL and self.config.enabled:
            handoff = build_handoff(
                reason,
                detail,
                self.steps,
                {"model_calls": self.usage.model_calls, "tool_calls": self.usage.tool_calls},
            )
        self.stop = StopEvent(
            reason, detail, answer or (handoff.render() if handoff else ""), handoff=handoff, **extra
        )
        self.tracer.add("stop", f"{reason.value} · {detail}", reason=reason.value)
        return self.stop


def _compact(obs: dict[str, Any]) -> str:
    text = json.dumps(obs, ensure_ascii=False)
    return text if len(text) <= 140 else text[:137] + "..."
