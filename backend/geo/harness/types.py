"""Shared harness types."""

from __future__ import annotations

from enum import StrEnum


class StopReason(StrEnum):
    """Why a run stopped. The first five are the stop conditions of Buổi 3."""

    GOAL = "GOAL"  # completion criteria passed (checked by code)
    BUDGET = "BUDGET"  # steps / tokens / time / money exhausted
    LOOP = "LOOP"  # repeated action or repeated failing observation
    STALL = "STALL"  # progress measure did not move
    NEEDS_HUMAN = "NEEDS_HUMAN"  # approval required or rejected
    UNGROUNDED = "UNGROUNDED"  # answer contains facts with no source
    UNVERIFIED = "UNVERIFIED"  # model said "done" but completion criteria failed
    MODEL_STOPPED = "MODEL_STOPPED"  # harness disabled: model's word is taken as is (baseline)
    ERROR = "ERROR"  # unexpected exception
