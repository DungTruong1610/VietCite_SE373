"""What the harness saw: every tool call with its normalised observation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Step:
    call_id: str
    tool: str
    args: dict[str, Any]
    obs: dict[str, Any]

    @property
    def ok(self) -> bool:
        return self.obs.get("status") == "ok"

    def short(self) -> str:
        return f"{self.tool}({json.dumps(self.args, ensure_ascii=False)}) → {self.obs.get('status')}"


@dataclass
class StepLog:
    steps: list[Step] = field(default_factory=list)

    def add(self, step: Step) -> None:
        self.steps.append(step)

    def of(self, tool: str, ok_only: bool = True) -> list[Step]:
        return [s for s in self.steps if s.tool == tool and (s.ok or not ok_only)]

    def observations_text(self) -> str:
        """All successful observations as text: the sources an answer may cite."""
        return "\n".join(json.dumps(s.obs, ensure_ascii=False) for s in self.steps if s.ok)

    def __len__(self) -> int:
        return len(self.steps)
