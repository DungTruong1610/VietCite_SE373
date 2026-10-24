"""Liveness and feature flags. Exposes booleans only, never key values."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app import __version__
from geo.config import get_settings

router = APIRouter(tags=["health"])


class Features(BaseModel):
    deepseek: bool
    jina: bool
    gemini: bool


class HealthResponse(BaseModel):
    status: str
    version: str
    features: Features
    offline: bool


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    s = get_settings()
    return HealthResponse(
        status="ok", version=__version__, features=Features(**s.features), offline=s.offline
    )
