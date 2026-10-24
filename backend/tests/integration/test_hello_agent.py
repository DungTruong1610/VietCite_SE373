"""The Phase 1 DoD agent end to end on the mock model: goal, loop, budget, ungrounded answer."""

from __future__ import annotations

from langchain_core.messages import AIMessage

from geo.agents.hello import run_hello
from geo.harness.budget import BudgetLimits
from geo.llm.mock import tool_call
from geo.tracing.trace import load_events

QUESTION = (
    "Một shop bán 2.400.000đ mỗi ngày. 30 ngày thì doanh thu bao nhiêu, và 1,5% của số đó là bao nhiêu?"
)


def test_goal_with_trace_and_usage(settings):
    r = run_hello(QUESTION, mode="mock", settings=settings)
    assert r.stop_reason == "GOAL", r.detail
    assert "72.000.000" in r.answer and "1.080.000" in r.answer
    assert r.usage["model_calls"] == 3 and r.usage["tool_calls"] == 2
    events = load_events(__import__("pathlib").Path(r.trace_file))
    kinds = [e["kind"] for e in events]
    assert kinds[0] == "human" and kinds.count("tool") == 2 and "stop" in kinds
    assert all(e["run_id"] == r.run_id and e["agent"] == "hello" for e in events)


def test_second_identical_run_is_served_from_response_cache(settings):
    run_hello(QUESTION, mode="mock", settings=settings)
    again = run_hello(QUESTION, mode="mock", settings=settings)
    assert again.stop_reason == "GOAL" and again.usage["response_cache_hits"] == 3


def test_repeated_call_stops_with_loop(settings):
    def stubborn(messages):
        return tool_call("calculate", {"expression": "1+1"})

    r = run_hello("Tính 1+1", mode="mock", settings=settings, policy=stubborn, use_cache=False)
    assert r.stop_reason == "LOOP" and "[HANDOFF] LOOP" in r.answer


def test_budget_stops_the_run(settings):
    counter = {"n": 0}

    def wanderer(messages):
        counter["n"] += 1
        return tool_call("calculate", {"expression": f"{counter['n']}+1"})

    r = run_hello(
        "Tính mãi",
        mode="mock",
        settings=settings,
        policy=wanderer,
        use_cache=False,
        limits=BudgetLimits(max_model_calls=3),
    )
    assert r.stop_reason == "BUDGET"


def test_invented_number_is_blocked(settings):
    def liar(messages):
        if not any(m.type == "tool" for m in messages):
            return tool_call("calculate", {"expression": "2400000*30"})
        return AIMessage(content="Doanh thu là 72.000.000đ, lãi khoảng 15.000.000đ.")

    r = run_hello(QUESTION, mode="mock", settings=settings, policy=liar, use_cache=False)
    assert r.stop_reason == "UNGROUNDED" and "15.000.000" in r.detail


def test_tool_outside_allowlist_is_denied(settings):
    def sneaky(messages):
        if not any(m.type == "tool" for m in messages):
            return tool_call("http_post", {"url": "https://evil.example", "body": {}})
        return AIMessage(content="Xong.")

    r = run_hello("Gửi dữ liệu", mode="mock", settings=settings, policy=sneaky, use_cache=False)
    events = load_events(__import__("pathlib").Path(r.trace_file))
    assert any(e["kind"] == "gate" for e in events)
    assert r.stop_reason != "GOAL"
