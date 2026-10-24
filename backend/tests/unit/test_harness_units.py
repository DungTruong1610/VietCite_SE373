"""Harness building blocks: contract, budget, loop detector, permission, grounding, handoff."""

from __future__ import annotations

from decimal import Decimal

from geo.harness.budget import Budget, BudgetLimits
from geo.harness.contract import enforce_contract
from geo.harness.grounding import check_numbers, extract_numbers, parse_number
from geo.harness.handoff import build_handoff
from geo.harness.loop_detector import LoopDetector
from geo.harness.permission import PermissionGate, PermissionPolicy, Verdict
from geo.harness.steps import Step, StepLog
from geo.harness.types import StopReason
from geo.llm.usage import Usage


# ------------------------------------------------------------------ contract
def test_contract_keeps_valid_status_and_wraps_the_rest():
    assert enforce_contract({"status": "ok", "x": 1}) == {"status": "ok", "x": 1}
    wrapped = enforce_contract({"error": "not found"})
    assert wrapped["status"] == "error" and wrapped["error"] == "unstructured_tool_output"
    assert "do NOT conclude" in wrapped["hint"]
    assert enforce_contract('{"status": "denied"}')["status"] == "denied"
    assert enforce_contract("free text")["status"] == "error"


# ------------------------------------------------------------------ budget (checked last)
def test_budget_reports_first_limit_reached():
    u = Usage(model_calls=3)
    assert Budget(BudgetLimits(max_model_calls=3), u).check().startswith("model called 3/3")
    assert Budget(BudgetLimits(max_model_calls=10), u).check() is None
    u.cost_usd = 0.2
    assert "cost" in Budget(BudgetLimits(max_model_calls=10, max_cost_usd=0.1), u).check()


# ------------------------------------------------------------------ loop detector
def test_loop_detector_flags_repeated_action():
    d = LoopDetector(repeat_k=2)
    assert d.check_action("calculate", {"expression": "1+1"}, {"status": "ok"}) is None
    assert "called 2 times" in d.check_action("calculate", {"expression": "1+1"}, {"status": "ok"})


def test_loop_detector_allows_one_retry_after_retryable_error():
    d = LoopDetector(repeat_k=2, allowed_retries=1)
    err = {"status": "error", "retryable": True}
    assert d.check_action("fetch", {"u": 1}, err) is None
    assert d.check_action("fetch", {"u": 1}, err) is None  # the allowed retry
    assert d.check_action("fetch", {"u": 1}, err) is not None


def test_loop_detector_polling_tools_are_exempt():
    d = LoopDetector(repeat_k=2, polling_tools=frozenset({"get_status"}))
    for _ in range(3):
        assert d.check_action("get_status", {"id": 1}, {"status": "ok", "n": _}) is None


def test_stall_detector():
    d = LoopDetector(stall_n=2)
    assert d.check_progress(1) is None
    assert d.check_progress(1) is None
    assert "stuck" in d.check_progress(1)


# ------------------------------------------------------------------ permission
POLICY = PermissionPolicy.from_dict(
    {
        "default": "deny",
        "agents": {"researcher": {"tools": ["fetch_page", "wp_publish_post", "http_post"]}},
        "rules": [
            {"tool": "wp_publish_post", "verdict": "ask", "reason": "irreversible"},
            {"tool": "http_post", "verdict": "deny", "reason": "exfiltration"},
        ],
    }
)


def test_permission_allowlist_is_least_privilege():
    gate = PermissionGate(POLICY)
    assert gate.gate("researcher", "fetch_page", {}).verdict is Verdict.ALLOW
    denied = gate.gate("writer", "fetch_page", {})
    assert denied.verdict is Verdict.DENY and denied.observation["error"] == "tool_not_allowed"


def test_permission_rules_deny_and_ask_and_remember_decision():
    gate = PermissionGate(POLICY)
    assert gate.gate("researcher", "http_post", {"url": "x"}).verdict is Verdict.DENY
    ask = gate.gate("researcher", "wp_publish_post", {"id": 1})
    assert ask.verdict is Verdict.ASK and ask.approval_key
    gate.record(ask.approval_key, True)
    assert gate.gate("researcher", "wp_publish_post", {"id": 1}).verdict is Verdict.ALLOW
    assert (
        gate.gate("researcher", "wp_publish_post", {"id": 2}).verdict is Verdict.ASK
    )  # other args: ask again


def test_policy_file_loads():
    from geo.agents.hello import POLICY_FILE

    policy = PermissionPolicy.from_yaml(POLICY_FILE)
    assert policy.allowed_tools("hello") == frozenset({"calculate"})
    assert policy.default is Verdict.DENY


# ------------------------------------------------------------------ grounding
def test_parse_vietnamese_and_json_numbers():
    assert parse_number("2.400.000") == Decimal("2400000")
    assert parse_number("1,5") == Decimal("1.5")
    assert parse_number("72000000.0") == Decimal("72000000.0")
    assert parse_number("1,234,567.5") == Decimal("1234567.5")


def test_extract_numbers_with_units_attached():
    tokens = [t for t, _ in extract_numbers("Bán 2.400.000đ mỗi ngày, thuế 1,5% trong 30 ngày")]
    assert tokens == ["2.400.000", "1,5", "30"]


def test_check_numbers_flags_invented_figures():
    sources = ["Hỏi: 2.400.000đ x 30 ngày", '{"status": "ok", "result": 72000000.0}']
    assert check_numbers("Doanh thu là 72.000.000đ", sources).ok
    rep = check_numbers("Doanh thu là 75.000.000đ, tăng 12%", sources)
    assert not rep.ok and rep.ungrounded == ["75.000.000", "12"]


# ------------------------------------------------------------------ handoff
def test_handoff_has_four_fields_and_one_question():
    log = StepLog([Step("c1", "calculate", {"expression": "1/0"}, {"status": "error"})])
    packet = build_handoff(StopReason.LOOP, "repeated", log, {"model_calls": 3})
    assert packet.tried and packet.state["model_calls"] == 3 and packet.question.endswith("?")
    assert "[HANDOFF] LOOP" in packet.render()
