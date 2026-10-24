"""Hello agent (Phase 1 DoD): ``create_agent`` + ``HarnessMiddleware`` + one tool (``calculate``).

It proves the foundation end to end before any real use case exists: gateway (DeepSeek or mock),
permission policy, loop/budget checks, numeric grounding, completion by code, JSONL trace, usage
and cost. It deliberately uses a calculator, not brand facts, so it invents nothing about Tallyo.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import Any, Literal

from langchain.agents import create_agent
from langchain_core.caches import BaseCache
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage

from geo.config import Settings, get_settings
from geo.context.prompt_layout import build_system_prompt, build_user_message
from geo.harness.budget import BudgetLimits
from geo.harness.completion import Check, CompletionResult
from geo.harness.core import Harness, HarnessConfig
from geo.harness.grounding import extract_numbers, parse_number
from geo.harness.middleware import HarnessMiddleware
from geo.harness.permission import PermissionGate, PermissionPolicy
from geo.harness.steps import StepLog
from geo.harness.types import StopReason
from geo.llm.cache import SQLiteResponseCache
from geo.llm.gateway import LLMGateway
from geo.llm.mock import tool_call
from geo.llm.usage import Usage
from geo.tools.calculator import CALCULATE
from geo.tools.registry import ToolRegistry
from geo.tracing.trace import TraceEvent, Tracer, new_id

AGENT = "hello"
POLICY_FILE = Path(__file__).resolve().parent.parent / "policies" / "permissions.yaml"
PERCENT = re.compile(r"(\d(?:[\d.,]*\d)?)\s*%")

SYSTEM_PROMPT = build_system_prompt(
    "Bạn là trợ lý tính toán của VietCite Studio (agent kiểm tra nền móng, Phase 1).",
    "Quy tắc:\n"
    "- Mọi phép tính PHẢI gọi tool `calculate`; không tự tính nhẩm.\n"
    "- Biểu thức chỉ gồm số thuần: không có dấu phân cách hàng nghìn, dùng dấu chấm cho phần thập phân "
    "(ví dụ 2400000*30*0.015).\n"
    "- Khi đã có đủ kết quả thì trả lời ngay, không gọi lại tool với cùng biểu thức.\n"
    "- Câu trả lời cuối bằng tiếng Việt, ngắn gọn. Chỉ dùng con số có trong câu hỏi hoặc trong kết quả "
    "tool (ưu tiên trường result_vi). Không đưa thêm con số nào khác.",
)


# ---------------------------------------------------------------------------- completion
class HelloCompletion:
    """Done when: a calculation succeeded, there is an answer, and it states the last result."""

    def check(self, steps: StepLog, answer: str | None) -> CompletionResult:
        calcs = steps.of("calculate")
        has_calc = bool(calcs)
        checks = [Check("calculate succeeded at least once", has_calc, f"{len(calcs)} ok call(s)")]
        if answer is None:
            return CompletionResult(False, checks + [Check("final answer present", False, "no answer yet")])
        checks.append(Check("final answer present", bool(answer.strip())))
        if has_calc:
            last = Decimal(str(calcs[-1].obs["result"]))
            stated = any(abs(v - last) <= Decimal("0.5") for _, v in extract_numbers(answer))
            checks.append(
                Check("answer states the last computed result", stated, calcs[-1].obs.get("result_vi", ""))
            )
        return CompletionResult.of(checks)


# ---------------------------------------------------------------------------- mock policy
def _question(messages: list[BaseMessage]) -> str:
    human = next((m for m in messages if isinstance(m, HumanMessage)), None)
    text = str(human.content) if human else ""
    m = re.search(r"<request>\s*(.*?)\s*</request>", text, flags=re.S)
    return m.group(1) if m else text


def _results(messages: list[BaseMessage]) -> list[dict[str, Any]]:
    out = []
    for m in messages:
        if isinstance(m, ToolMessage):
            try:
                obs = json.loads(str(m.content))
            except json.JSONDecodeError:
                continue
            if obs.get("status") == "ok":
                out.append(obs)
    return out


def mock_policy(messages: list[BaseMessage]) -> AIMessage:
    """Deterministic stand-in for the LLM: multiply the plain numbers, then apply the percentage."""
    question = _question(messages)
    percents = [v for tok in PERCENT.findall(question) if (v := parse_number(tok)) is not None]
    plain = [v for tok, v in extract_numbers(question) if v not in percents]
    done = _results(messages)
    if not done and plain:
        return tool_call("calculate", {"expression": "*".join(str(v) for v in plain)})
    if len(done) == 1 and percents:
        return tool_call("calculate", {"expression": f"{done[0]['result']}*{percents[0]}/100"})
    if not done:
        return AIMessage(content="Câu hỏi không có con số nào để tính.")
    parts = [f"kết quả là {done[0]['result_vi']}"]
    if len(done) > 1:
        parts.append(f"{str(percents[0]).replace('.', ',')}% của số đó là {done[1]['result_vi']}")
    return AIMessage(content="Theo phép tính bằng tool, " + "; ".join(parts) + ".")


# ---------------------------------------------------------------------------- run
@dataclass
class HelloResult:
    run_id: str
    mode: str
    model: str
    stop_reason: str
    detail: str
    answer: str
    usage: dict[str, Any]
    trace_file: str
    events: list[TraceEvent] = field(default_factory=list)

    def done_payload(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "stop_reason": self.stop_reason,
            "answer": self.answer,
            "usage": self.usage,
            "trace_file": self.trace_file,
        }


def run_hello(
    question: str,
    *,
    mode: Literal["mock", "live"] = "mock",
    settings: Settings | None = None,
    sink: Callable[[TraceEvent], None] | None = None,
    limits: BudgetLimits | None = None,
    cache: BaseCache | None = None,
    use_cache: bool = True,
    policy: Callable[[list[BaseMessage]], AIMessage] = mock_policy,
) -> HelloResult:
    settings = settings or get_settings()
    usage = Usage()
    run_id = new_id("run_")
    trace_path = settings.data_dir / "traces" / f"{run_id}.jsonl"
    tracer = Tracer(run_id, trace_path, sink)
    if cache is None and use_cache:
        cache = SQLiteResponseCache(settings.data_dir / "llm_cache.sqlite")

    registry = ToolRegistry([CALCULATE])
    permission_policy = PermissionPolicy.from_yaml(POLICY_FILE)
    harness = Harness(
        AGENT,
        registry,
        PermissionGate(permission_policy),
        usage,
        tracer,
        HarnessConfig(limits=limits or BudgetLimits(max_model_calls=8, max_cost_usd=0.02)),
        completion=HelloCompletion(),
        request_text=question,
    )
    gateway = LLMGateway(settings, usage, cache)
    model = gateway.chat_model(
        "agent",
        mock_policy=policy,
        mock_name="hello",
        force_mock=(mode == "mock"),
        require_real=(mode == "live"),
    )
    model_name = getattr(model, "model_name", None) or "mock"
    agent = create_agent(
        model=model,
        tools=registry.langchain_tools(permission_policy.allowed_tools(AGENT)),
        system_prompt=SYSTEM_PROMPT,
        middleware=[HarnessMiddleware(harness)],
    )

    with tracer.span(AGENT, "react"):
        tracer.add("human", question, mode=mode, model=model_name)
        last_text = ""
        try:
            state = agent.invoke({"messages": [build_user_message(question)]}, config={"recursion_limit": 30})
            last_text = str(state["messages"][-1].content)
        except Exception as exc:  # report, never crash the caller
            harness.fail(StopReason.ERROR, f"{type(exc).__name__}: {exc}")
        stop = harness.stop or harness.finalize(last_text)
        tracer.add("harness", "usage", **usage.summary())

    return HelloResult(
        run_id,
        mode,
        model_name,
        stop.reason.value,
        stop.detail,
        stop.answer,
        usage.summary(),
        str(trace_path),
        tracer.events,
    )
