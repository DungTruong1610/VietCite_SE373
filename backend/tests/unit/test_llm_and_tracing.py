"""Usage/cost, response cache, prompt layout, trace and audit log."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, LLMResult

from geo.config import Price
from geo.context.prompt_layout import VolatilePrefixError, build_messages, build_system_prompt
from geo.llm.cache import SQLiteResponseCache, normalize_prompt
from geo.llm.mock import MockChatModel
from geo.llm.usage import Usage, UsageCallback, cost_of
from geo.tracing.audit import AuditLog
from geo.tracing.trace import Tracer, first_bad_event, load_events, redact


# ------------------------------------------------------------------ usage and cost
def test_cost_separates_prompt_cache_hits():
    price = Price(input=1.0, output=4.0, cached_input=0.1)
    assert cost_of(price, 1_000_000, 0, 0) == pytest.approx(1.0)
    assert cost_of(price, 1_000_000, 0, 1_000_000) == pytest.approx(0.1)


def _result(msg: AIMessage) -> LLMResult:
    return LLMResult(generations=[[ChatGeneration(message=msg)]])


def test_usage_callback_reads_deepseek_cache_fields():
    usage = Usage()
    cb = UsageCallback(usage, Price(1.0, 2.0, 0.1), "deepseek-chat")
    msg = AIMessage(
        content="ok",
        usage_metadata={"input_tokens": 1000, "output_tokens": 100, "total_tokens": 1100},
        response_metadata={"token_usage": {"prompt_cache_hit_tokens": 800}},
    )
    cb.on_llm_end(_result(msg))
    assert usage.cached_tokens == 800 and usage.cache_hit_rate == pytest.approx(0.8)
    assert usage.cost_usd == pytest.approx((200 * 1.0 + 800 * 0.1 + 100 * 2.0) / 1e6)


def test_usage_callback_counts_response_cache_hit_as_free():
    usage = Usage()
    cb = UsageCallback(usage, Price(1.0, 2.0, 0.1), "deepseek-chat")
    msg = AIMessage(
        content="ok",
        usage_metadata={"input_tokens": 1000, "output_tokens": 100, "total_tokens": 1100},
        response_metadata={"response_cache_hit": True},
    )
    cb.on_llm_end(_result(msg))
    assert usage.response_cache_hits == 1 and usage.cost_usd == 0 and usage.tokens_in == 0


# ------------------------------------------------------------------ response cache
def test_normalize_prompt_ignores_run_specific_ids():
    a = json.dumps(
        [
            {
                "lc": 1,
                "type": "constructor",
                "id": ["x", "AIMessage"],
                "kwargs": {"content": "", "id": "lc_run--1", "tool_calls": [{"id": "call_ab", "name": "t"}]},
            },
            {
                "lc": 1,
                "type": "constructor",
                "id": ["x", "ToolMessage"],
                "kwargs": {"content": "r", "tool_call_id": "call_ab"},
            },
        ]
    )
    b = a.replace("lc_run--1", "lc_run--2").replace("call_ab", "call_zz")
    assert normalize_prompt(a) == normalize_prompt(b)
    assert normalize_prompt(a) != normalize_prompt(a.replace('"r"', '"other"'))


def test_mock_model_replays_from_sqlite_cache(tmp_path: Path):
    cache = SQLiteResponseCache(tmp_path / "c.sqlite")
    calls = []

    def policy(messages):
        calls.append(1)
        return AIMessage(content="xin chào")

    model = MockChatModel(policy=policy, cache=cache)
    first = model.invoke([HumanMessage(content="hi")])
    second = model.invoke([HumanMessage(content="hi")])
    assert len(calls) == 1 and cache.size() == 1
    assert second.content == first.content and second.response_metadata.get("response_cache_hit") is True


# ------------------------------------------------------------------ prompt layout (Buổi 7)
def test_static_prefix_rejects_volatile_content():
    with pytest.raises(VolatilePrefixError):
        build_system_prompt("Bạn là trợ lý.", "Hôm nay 2026-10-24 10:30")
    messages = build_messages(build_system_prompt("Bạn là trợ lý."), "Câu hỏi", {"brand": "Tallyo"})
    assert messages[0].type == "system" and "<brand>" in str(messages[1].content)
    assert str(messages[1].content).endswith("</request>")


# ------------------------------------------------------------------ trace
def test_trace_redacts_secrets_and_writes_jsonl(tmp_path: Path):
    seen = []
    tracer = Tracer(path=tmp_path / "t.jsonl", sink=seen.append)
    with tracer.span("hello", "react"):
        tracer.add(
            "tool", "calling with sk-" + "a" * 32, headers={"Authorization": "Bearer abc"}, status="ok"
        )
        tracer.add("gate", "blocked", status="denied")
    events = load_events(tmp_path / "t.jsonl")
    assert len(events) == 2 and len(seen) == 2
    raw = (tmp_path / "t.jsonl").read_text(encoding="utf-8")
    assert "sk-aaaa" not in raw and "Bearer abc" not in raw
    assert events[0]["agent"] == "hello" and events[0]["node"] == "react"
    assert first_bad_event(events)["kind"] == "gate"
    assert redact({"api_key": "x", "nested": [{"token": "y"}]}) == {
        "api_key": "***",
        "nested": [{"token": "***"}],
    }


# ------------------------------------------------------------------ audit log
def test_audit_log_detects_tampering(tmp_path: Path):
    log = AuditLog(tmp_path / "audit.jsonl")
    log.append("approver", "approve", "run_1", article_hash="abc")
    log.append("system", "publish", "run_1", post_id=7)
    assert log.verify().ok
    lines = (tmp_path / "audit.jsonl").read_text(encoding="utf-8").splitlines()
    tampered = json.loads(lines[0])
    tampered["actor"] = "editor"
    (tmp_path / "audit.jsonl").write_text(json.dumps(tampered) + "\n" + lines[1] + "\n", encoding="utf-8")
    result = log.verify()
    assert not result.ok and result.broken_at == 1
