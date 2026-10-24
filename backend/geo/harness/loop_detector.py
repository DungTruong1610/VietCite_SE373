"""Three-signal loop detector (ported from Buổi 3).

1. repeated action       same (tool, args) again within the last ``window`` steps
2. repeated observation  different args but the same failing result
3. no progress           the task's progress measure did not change for ``stall_n`` steps

A retry right after a ``retryable`` error is allowed ``allowed_retries`` times. Polling tools are
exempt from signal 1. A write tool changes the world, so earlier reads stop counting as repeats.
"""

from __future__ import annotations

import json
from collections import deque
from collections.abc import Hashable
from typing import Any

RETRY_GAP = 2


def fingerprint(tool: str, args: dict[str, Any]) -> tuple[str, str]:
    return tool, json.dumps(args, sort_keys=True, ensure_ascii=False)


class LoopDetector:
    def __init__(
        self,
        window: int = 6,
        repeat_k: int = 2,
        same_obs_k: int = 4,
        stall_n: int = 5,
        allowed_retries: int = 1,
        polling_tools: frozenset[str] = frozenset(),
        write_tools: frozenset[str] = frozenset(),
    ) -> None:
        self.recent: deque[tuple[str, str]] = deque(maxlen=window)
        self.obs: deque[str] = deque(maxlen=window)
        self.k, self.k_obs, self.n = repeat_k, same_obs_k, stall_n
        self.allowed_retries = allowed_retries
        self.polling, self.writes = polling_tools, write_tools
        self.retries: dict[tuple[str, str], int] = {}
        self.retryable: dict[tuple[str, str], bool] = {}
        self.last_progress: Hashable | None = None
        self.stall = 0

    def check_action(self, tool: str, args: dict[str, Any], observation: dict[str, Any]) -> str | None:
        fp = fingerprint(tool, args)
        seen = self.recent.count(fp)
        is_retry = fp in list(self.recent)[-RETRY_GAP:] and self.retryable.get(fp, False)
        alarm = None
        if tool not in self.polling and seen + 1 >= self.k:
            used = self.retries.get(fp, 0)
            if is_retry and used < self.allowed_retries:
                self.retries[fp] = used + 1
            else:
                alarm = f"'{tool}' called {seen + 1} times with the same args in the last {self.recent.maxlen} steps"
        if tool in self.writes:
            kept = [x for x in self.recent if x[0] in self.writes]
            self.recent.clear()
            self.recent.extend(kept)
            self.obs.clear()
        self.recent.append(fp)
        self.retryable[fp] = bool(observation.get("retryable"))
        if alarm:
            return alarm
        ofp = json.dumps(observation, sort_keys=True, ensure_ascii=False)
        if observation.get("status") != "ok" and self.obs.count(ofp) + 1 >= self.k_obs:
            return f"{self.obs.count(ofp) + 1} calls with different args returned the same error"
        self.obs.append(ofp)
        return None

    def check_progress(self, progress: Hashable) -> str | None:
        self.stall = self.stall + 1 if progress == self.last_progress else 0
        self.last_progress = progress
        if self.stall >= self.n:
            return f"progress stuck at {progress!r} for {self.stall} steps"
        return None
