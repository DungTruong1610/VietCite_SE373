"""Permission gate: checked BEFORE a tool runs (generalised from Buổi 3).

The policy is data (YAML), not code, so security rules can be reviewed without reading Python:

    default: deny            # a tool not listed for an agent is denied
    agents:
      hello:
        tools: [calculate]
    rules:                   # verdicts that apply to every agent that may use the tool
      - tool: wp_publish_post
        verdict: ask         # needs a human decision
        reason: "publishing cannot be undone"

Order in ``PermissionGate.gate``:
    a. allowlist of the agent (least privilege)
    b. tool rules: deny / ask / allow
    c. a human decision already recorded for this exact action is reused (asked only once)
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml


class Verdict(StrEnum):
    ALLOW = "allow"
    DENY = "deny"
    ASK = "ask"


@dataclass(frozen=True)
class ToolRule:
    tool: str
    verdict: Verdict
    reason: str = ""


@dataclass(frozen=True)
class PermissionPolicy:
    agents: dict[str, frozenset[str]] = field(default_factory=dict)
    rules: dict[str, ToolRule] = field(default_factory=dict)
    default: Verdict = Verdict.DENY

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PermissionPolicy:
        agents = {name: frozenset(spec.get("tools", [])) for name, spec in (data.get("agents") or {}).items()}
        rules = {}
        for r in data.get("rules") or []:
            rule = ToolRule(r["tool"], Verdict(r["verdict"]), r.get("reason", ""))
            rules[rule.tool] = rule
        return cls(agents, rules, Verdict(data.get("default", "deny")))

    @classmethod
    def from_yaml(cls, path: Path) -> PermissionPolicy:
        return cls.from_dict(yaml.safe_load(path.read_text(encoding="utf-8")) or {})

    def allowed_tools(self, agent: str) -> frozenset[str]:
        return self.agents.get(agent, frozenset())


@dataclass
class GateDecision:
    verdict: Verdict
    observation: dict[str, Any] | None = None  # returned to the model when not allowed
    reason: str = ""
    approval_key: str | None = None


def approval_key(agent: str, tool: str, args: dict[str, Any]) -> str:
    return f"{agent}:{tool}:{json.dumps(args, sort_keys=True, ensure_ascii=False)}"


class PermissionGate:
    def __init__(self, policy: PermissionPolicy) -> None:
        self.policy = policy
        self.approvals: dict[str, bool] = {}

    def record(self, key: str, approved: bool) -> None:
        self.approvals[key] = approved

    def gate(self, agent: str, tool: str, args: dict[str, Any]) -> GateDecision:
        allowed = self.policy.allowed_tools(agent)
        if tool not in allowed and self.policy.default is not Verdict.ALLOW:
            return GateDecision(
                Verdict.DENY,
                {
                    "status": "denied",
                    "error": "tool_not_allowed",
                    "tool": tool,
                    "hint": f"Agent '{agent}' may only call: {sorted(allowed)}",
                },
                reason="not in allowlist",
            )
        rule = self.policy.rules.get(tool)
        if rule is None or rule.verdict is Verdict.ALLOW:
            return GateDecision(Verdict.ALLOW)
        if rule.verdict is Verdict.DENY:
            return GateDecision(
                Verdict.DENY,
                {
                    "status": "denied",
                    "error": "tool_forbidden",
                    "tool": tool,
                    "hint": rule.reason or "This tool is forbidden by policy",
                },
                reason=rule.reason,
            )
        key = approval_key(agent, tool, args)
        if key in self.approvals:
            if self.approvals[key]:
                return GateDecision(Verdict.ALLOW, approval_key=key)
            return GateDecision(
                Verdict.DENY,
                {"status": "denied", "error": "approval_rejected", "hint": "A human rejected this action"},
                reason="rejected by human",
                approval_key=key,
            )
        return GateDecision(
            Verdict.ASK,
            {
                "status": "pending",
                "error": "approval_required",
                "hint": rule.reason or "Waiting for a human decision",
            },
            reason=rule.reason,
            approval_key=key,
        )
