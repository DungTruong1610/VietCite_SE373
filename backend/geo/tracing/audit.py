"""Append-only audit log for decisions that matter (approve, reject, publish).

Each entry stores the hash of the previous entry, so editing or deleting a past line breaks the
chain and ``verify`` reports where. This is the "logging" harness layer: we do not have to trust
what an agent says it did.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from geo.tracing.trace import redact

GENESIS = "0" * 64


def _digest(entry: dict[str, Any]) -> str:
    body = {k: v for k, v in entry.items() if k != "hash"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class VerifyResult:
    ok: bool
    entries: int
    broken_at: int | None = None  # 1-based line number of the first bad entry
    reason: str = ""


class AuditLog:
    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)

    def _last_hash(self) -> str:
        lines = [x for x in self.path.read_text(encoding="utf-8").splitlines() if x.strip()]
        return json.loads(lines[-1])["hash"] if lines else GENESIS

    def append(self, actor: str, action: str, target: str, **details: Any) -> dict[str, Any]:
        entry: dict[str, Any] = {
            "ts": datetime.now(UTC).isoformat(timespec="milliseconds"),
            "actor": actor,
            "action": action,
            "target": target,
            "details": redact(details),
            "prev_hash": self._last_hash(),
        }
        entry["hash"] = _digest(entry)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return entry

    def verify(self) -> VerifyResult:
        prev = GENESIS
        lines = [x for x in self.path.read_text(encoding="utf-8").splitlines() if x.strip()]
        for i, line in enumerate(lines, start=1):
            entry = json.loads(line)
            if entry.get("prev_hash") != prev:
                return VerifyResult(False, len(lines), i, "prev_hash does not match the previous entry")
            if entry.get("hash") != _digest(entry):
                return VerifyResult(False, len(lines), i, "entry content was modified")
            prev = entry["hash"]
        return VerifyResult(True, len(lines))
