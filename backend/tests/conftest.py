"""Shared fixtures. Tests never call real APIs: keys are removed and offline mode is forced."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from geo.config import Settings, get_settings, load_settings

SECRET_VARS = (
    "DEEPSEEK_API_KEY",
    "JINA_API_KEY",
    "GEMINI_API_KEY",
    "JWT_SECRET",
    "APPROVAL_TOKEN_SECRET",
    "SEED_EDITOR_PASSWORD",
    "SEED_APPROVER_PASSWORD",
)


@pytest.fixture(autouse=True)
def offline_env(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> Iterator[None]:
    """Unit/integration tests: no keys, offline, data under a temp dir. Live tests keep the real env."""
    if request.node.get_closest_marker("live"):
        yield
        return
    for var in SECRET_VARS:
        monkeypatch.setenv(var, "")
    monkeypatch.setenv("GEO_OFFLINE", "true")
    monkeypatch.setenv("GEO_DATA_DIR", str(tmp_path / "data"))
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return load_settings(env_file=tmp_path / "missing.env")
