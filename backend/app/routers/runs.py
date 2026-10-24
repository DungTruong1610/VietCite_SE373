"""Demo run streamed as Server-Sent Events (Phase 1: the hello agent).

The agent runs in a worker thread; each trace event is pushed to a queue as soon as it is recorded
and forwarded to the browser:

    event: trace   data: {run_id, span_id, seq, agent, node, kind, text, data, ts}
    event: done    data: {run_id, stop_reason, answer, usage, trace_file}
    event: error   data: {message}
"""

from __future__ import annotations

import asyncio
import json
import logging
import queue
import threading
from dataclasses import asdict
from typing import Annotated, Any, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sse_starlette.sse import EventSourceResponse

from app.security import User, current_user
from geo.agents.hello import run_hello
from geo.config import get_settings
from geo.tracing.trace import TraceEvent

router = APIRouter(prefix="/runs", tags=["runs"])
log = logging.getLogger("vietcite.runs")
_DONE = object()


def _json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, default=str)


@router.get("/demo/stream")
async def demo_stream(
    user: Annotated[User, Depends(current_user)],
    mode: Literal["mock", "live"] = "mock",
    question: str = Query(min_length=1, max_length=500),
) -> EventSourceResponse:
    settings = get_settings()
    if mode == "live" and not settings.features["deepseek"]:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Chế độ live cần DEEPSEEK_API_KEY và GEO_OFFLINE=false"
        )
    events: queue.Queue[Any] = queue.Queue()

    def sink(event: TraceEvent) -> None:
        events.put(("trace", asdict(event)))

    def worker() -> None:
        try:
            result = run_hello(question, mode=mode, settings=settings, sink=sink)
            events.put(("done", result.done_payload()))
        except Exception as exc:  # the stream must always end with done or error
            log.exception("demo run failed")
            events.put(("error", {"message": f"{type(exc).__name__}"}))
        finally:
            events.put(_DONE)

    threading.Thread(target=worker, name="demo-run", daemon=True).start()
    log.info("demo run started by %s (mode=%s)", user.username, mode)

    async def stream():
        while True:
            item = await asyncio.to_thread(events.get)
            if item is _DONE:
                break
            kind, data = item
            yield {"event": kind, "data": _json(data)}

    return EventSourceResponse(stream())
