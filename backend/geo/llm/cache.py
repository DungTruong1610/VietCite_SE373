"""Response cache on SQLite: replay a model answer when the exact same request was made before.

Purpose: reproducible evals and a CI that never spends money. This is NOT the provider's prompt
cache (see ``geo.llm.usage``). Plugged into LangChain through ``BaseCache``, so it works for any
chat model passed to ``create_agent`` via the model's ``cache=`` field.

Replayed answers are marked with ``response_metadata["response_cache_hit"] = True`` so usage
accounting counts them as free.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import threading
import warnings
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from langchain_core._api.beta_decorator import LangChainBetaWarning
from langchain_core.caches import RETURN_VAL_TYPE, BaseCache
from langchain_core.load import dumps, loads
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, Generation

VOLATILE_KWARGS = ("id", "response_metadata", "usage_metadata")


def normalize_prompt(prompt: str) -> str:
    """Drop per-run noise from a serialized conversation so identical runs share cache keys.

    LangChain serializes the messages as the cache prompt. Message ids (``lc_run--…``), provider
    response metadata and random tool-call ids differ on every run although the conversation is
    the same; they are removed or replaced by their order of appearance. Content is untouched.
    """
    try:
        messages = json.loads(prompt)
    except json.JSONDecodeError:
        return prompt
    if not isinstance(messages, list):
        return prompt
    call_ids: dict[str, str] = {}

    def stable(call_id: Any) -> str:
        return call_ids.setdefault(str(call_id), f"call_{len(call_ids)}")

    for msg in messages:
        kwargs = msg.get("kwargs") if isinstance(msg, dict) else None
        if not isinstance(kwargs, dict):
            continue
        for key in VOLATILE_KWARGS:
            kwargs.pop(key, None)
        for call in kwargs.get("tool_calls") or []:
            call["id"] = stable(call.get("id"))
        kwargs.pop("additional_kwargs", None)
        if "tool_call_id" in kwargs:
            kwargs["tool_call_id"] = stable(kwargs["tool_call_id"])
    return json.dumps(messages, sort_keys=True, ensure_ascii=False)


def _key(prompt: str, llm_string: str) -> str:
    return hashlib.sha256(f"{llm_string}\x00{normalize_prompt(prompt)}".encode()).hexdigest()


class SQLiteResponseCache(BaseCache):
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self._lock = threading.Lock()
        with self._connect() as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS responses ("
                "key TEXT PRIMARY KEY, value TEXT NOT NULL, created_at TEXT NOT NULL)"
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path, check_same_thread=False)

    def lookup(self, prompt: str, llm_string: str) -> RETURN_VAL_TYPE | None:
        with self._lock, self._connect() as db:
            row = db.execute(
                "SELECT value FROM responses WHERE key = ?", (_key(prompt, llm_string),)
            ).fetchone()
        if not row:
            return None
        # Only rebuild the classes a cached answer can contain, never arbitrary objects.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", LangChainBetaWarning)
            generations: list[Generation] = loads(
                row[0], allowed_objects=[Generation, ChatGeneration, AIMessage]
            )
        for gen in generations:
            if isinstance(gen, ChatGeneration):
                gen.message.response_metadata = {**gen.message.response_metadata, "response_cache_hit": True}
        return generations

    def update(self, prompt: str, llm_string: str, return_val: Sequence[Generation]) -> None:
        value = dumps(list(return_val))
        with self._lock, self._connect() as db:
            db.execute(
                "INSERT OR REPLACE INTO responses (key, value, created_at) VALUES (?, ?, ?)",
                (_key(prompt, llm_string), value, datetime.now(UTC).isoformat()),
            )

    def clear(self, **kwargs: Any) -> None:
        with self._lock, self._connect() as db:
            db.execute("DELETE FROM responses")

    def size(self) -> int:
        with self._lock, self._connect() as db:
            return int(db.execute("SELECT COUNT(*) FROM responses").fetchone()[0])
