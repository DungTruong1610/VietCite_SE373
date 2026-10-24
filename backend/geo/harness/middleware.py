"""Plug the harness into LangChain 1.x ``create_agent`` (ported from Buổi 3).

One hook per stage of the agent loop:

    after_model     the model proposed tool calls → check permission BEFORE the tools run;
                    a decision needs a person → ``interrupt()``;
                    the model stopped calling tools → grounding + completion checks.
    wrap_tool_call  the harness runs the tool: schema, allowlist, ``status`` envelope, step log.
    before_model    an observation arrived → checklist 1–4 before paying for another model call.

A hook that finds a stop condition returns ``{"jump_to": "end"}`` with the hand-off as the answer.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from langchain.agents.middleware import AgentMiddleware, hook_config
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import interrupt

from geo.harness.core import Harness
from geo.harness.permission import Verdict
from geo.harness.types import StopReason
from geo.tracing.trace import fmt_call


class HarnessMiddleware(AgentMiddleware):
    def __init__(self, harness: Harness) -> None:
        super().__init__()
        self.h = harness
        self._traced: set[str] = set()

    def _end(self) -> dict[str, Any]:
        assert self.h.stop is not None
        return {"jump_to": "end", "messages": [AIMessage(content=self.h.stop.answer)]}

    @hook_config(can_jump_to=["end"])
    def before_model(self, state: Any, runtime: Any) -> dict[str, Any] | None:
        return self._end() if self.h.checkpoint() else None

    @hook_config(can_jump_to=["end"])
    def after_model(self, state: Any, runtime: Any) -> dict[str, Any] | None:
        last = state["messages"][-1]
        calls = getattr(last, "tool_calls", None) or []
        self._trace_ai(last, calls)
        if not calls:
            stop = self.h.finalize(str(last.content))
            if stop.reason in (StopReason.GOAL, StopReason.MODEL_STOPPED) and stop.answer == last.content:
                return None
            return self._end()
        for c in calls:
            decision = self.h.review(c["name"], c["args"])
            if decision.verdict is Verdict.ASK and decision.approval_key:
                answer = interrupt(
                    {"type": "approval", "tool": c["name"], "args": c["args"], "reason": decision.reason}
                )
                self.h.resolve(decision.approval_key, bool(answer.get("approved")), c["name"])
            if self.h.stop:
                return self._end()
        return None

    def wrap_tool_call(self, request: Any, handler: Callable[[Any], Any]) -> ToolMessage:
        c = request.tool_call

        def run_framework_tool() -> Any:
            return handler(request).content

        obs = self.h.run_tool(c["id"], c["name"], c["args"], executor=run_framework_tool)
        return ToolMessage(content=json.dumps(obs, ensure_ascii=False), tool_call_id=c["id"], name=c["name"])

    def _trace_ai(self, msg: Any, calls: list[dict[str, Any]]) -> None:
        key = msg.id or str(id(msg))
        if key in self._traced:
            return
        self._traced.add(key)
        if calls:
            for c in calls:
                self.h.tracer.add("ai", fmt_call(c["name"], c["args"]), tool=c["name"], args=c["args"])
        else:
            self.h.tracer.add("ai", str(msg.content))
