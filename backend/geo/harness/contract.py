"""Tool output contract: every observation carries an explicit ``status`` (ported from Buổi 3).

An observation without a status (``{}``, ``{"error": "not found"}``, free text) is never handed to
the model as is: the harness wraps it as a structured error that says NOT to conclude "there is no
data" from it (failure mode "trusting bad data").
"""

from __future__ import annotations

import json
from typing import Any

VALID = {"ok", "error", "denied", "invalid_param", "pending"}


def ok(**data: Any) -> dict[str, Any]:
    return {"status": "ok", **data}


def error(code: str, hint: str, retryable: bool = False, **data: Any) -> dict[str, Any]:
    return {"status": "error", "error": code, "hint": hint, "retryable": retryable, **data}


def enforce_contract(raw: Any) -> dict[str, Any]:
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            raw = {"text": raw}
    if isinstance(raw, dict) and raw.get("status") in VALID:
        return raw
    return {
        "status": "error",
        "error": "unstructured_tool_output",
        "retryable": True,
        "raw": raw,
        "hint": (
            "Tool output has no explicit status: do NOT conclude 'no data'. "
            "Call it once more or hand off to a human."
        ),
    }


def parse_observation(raw: Any) -> dict[str, Any]:
    """Read a raw observation without normalising it (used by the no-harness baseline)."""
    if isinstance(raw, dict):
        return raw
    try:
        val = json.loads(raw)
        return val if isinstance(val, dict) else {"value": val}
    except (TypeError, json.JSONDecodeError):
        return {"text": str(raw)}
