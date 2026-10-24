"""Run trace: one JSONL event per step, grouped by run → span (agent, node).

Every event goes to an optional ``sink`` as soon as it is recorded (used by the API to stream
SSE), and to ``<data_dir>/traces/<run_id>.jsonl`` when a path is given.

Secrets never reach a trace: ``redact`` masks values under sensitive keys and strings that
look like API keys before an event is stored.

CLI (step 2 "locate" of the debug process from Buổi 3):
    python -m geo.tracing.trace <file.jsonl>            # print the whole trace
    python -m geo.tracing.trace <file.jsonl> --locate   # print the first bad event
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SENSITIVE_KEY = re.compile(r"(authorization|api[_-]?key|secret|password|token)", re.IGNORECASE)
SECRET_VALUE = re.compile(r"\b(sk-[A-Za-z0-9]{16,}|jina_[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,})\b")
BAD_KINDS = {"gate", "approval", "error"}
MASK = "***"


def new_id(prefix: str = "") -> str:
    return prefix + uuid.uuid4().hex[:12]


def redact(value: Any) -> Any:
    """Deep copy of ``value`` with secrets masked."""
    if isinstance(value, dict):
        return {k: (MASK if SENSITIVE_KEY.search(str(k)) else redact(v)) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [redact(v) for v in value]
    if isinstance(value, str):
        return SECRET_VALUE.sub(MASK, value)
    return value


@dataclass
class TraceEvent:
    run_id: str
    span_id: str
    seq: int
    agent: str
    node: str
    kind: str  # human · ai · tool · gate · approval · harness · stop · error
    text: str
    data: dict[str, Any] = field(default_factory=dict)
    ts: str = field(default_factory=lambda: datetime.now(UTC).isoformat(timespec="milliseconds"))

    def line(self) -> str:
        body = self.text if len(self.text) <= 140 else self.text[:137] + "..."
        return f"#{self.seq:<4}{self.kind:<9}{self.node:<14}{body}"


class Tracer:
    """Records the events of one run."""

    def __init__(
        self,
        run_id: str | None = None,
        path: Path | None = None,
        sink: Callable[[TraceEvent], None] | None = None,
    ) -> None:
        self.run_id = run_id or new_id("run_")
        self.path = path
        self.sink = sink
        self.events: list[TraceEvent] = []
        self._span = ("main", "main", new_id("sp_"))
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("", encoding="utf-8")

    @contextmanager
    def span(self, agent: str, node: str) -> Iterator[str]:
        """Group the events emitted inside the block under one span (agent + graph node)."""
        previous = self._span
        self._span = (agent, node, new_id("sp_"))
        try:
            yield self._span[2]
        finally:
            self._span = previous

    def add(self, kind: str, text: str, **data: Any) -> TraceEvent:
        agent, node, span_id = self._span
        event = TraceEvent(
            self.run_id, span_id, len(self.events) + 1, agent, node, kind, redact(text), redact(data)
        )
        self.events.append(event)
        if self.path:
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(asdict(event), ensure_ascii=False, default=str) + "\n")
        if self.sink:
            self.sink(event)
        return event

    def render(self) -> str:
        return "\n".join(e.line() for e in self.events)


def fmt_call(tool: str, args: dict[str, Any]) -> str:
    return f"{tool}(" + ", ".join(f"{k}={v!r}" for k, v in args.items()) + ")"


def load_events(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def first_bad_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    """First event where something went wrong: a tool error, a blocked call or an approval."""
    for e in events:
        if e["kind"] == "tool" and e["data"].get("status") not in (None, "ok"):
            return e
        if e["kind"] in BAD_KINDS:
            return e
    return None


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    parser = argparse.ArgumentParser(description="Read a trace JSONL file and locate the first bad event")
    parser.add_argument("path", type=Path)
    parser.add_argument("--locate", action="store_true", help="only print the first bad event")
    args = parser.parse_args(argv)
    events = load_events(args.path)
    if not args.locate:
        print("\n".join(TraceEvent(**e).line() for e in events))
        return 0
    bad = first_bad_event(events)
    print(
        f"First bad event: #{bad['seq']} {bad['kind']} [{bad['agent']}/{bad['node']}] {bad['text']}"
        if bad
        else "No bad event in this trace."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
