"""Runtime configuration read from environment (``.env`` at the repo root).

Rules:
- Keys are read here and nowhere else; they are never logged or returned by the API.
- A missing key disables the feature that needs it (``Settings.features``) instead of crashing,
  so the whole system still runs offline with the mock model and cached responses.
- Models are chosen per *role* (writer, extractor, judge...), not per call site.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BACKEND_DIR.parent
DATA_DIR = BACKEND_DIR / ".data"  # runtime files (cache, traces, sqlite); git-ignored

ROLES = ("agent", "writer", "extractor", "judge", "reasoner")


@dataclass(frozen=True)
class Price:
    """USD per 1M tokens. ``cached_input`` is the price of prompt-cache hits."""

    input: float
    output: float
    cached_input: float


# Assumed list prices, used only to estimate cost. Check the provider's pricing page before
# reporting numbers; override with GEO_PRICE_<MODEL>="input,output,cached_input" if they change.
DEFAULT_PRICES: dict[str, Price] = {
    "deepseek-chat": Price(0.27, 1.10, 0.07),
    "deepseek-reasoner": Price(0.55, 2.19, 0.14),
    "mock": Price(0.0, 0.0, 0.0),
}
UNKNOWN_PRICE = Price(1.0, 4.0, 0.25)  # conservative fallback for unlisted models


@dataclass(frozen=True)
class Settings:
    # Secret fields use repr=False: a Settings object printed in a log, traceback or failing test
    # must never show a key value.
    deepseek_api_key: str | None = field(repr=False)
    deepseek_base_url: str
    deepseek_model: str
    deepseek_reasoning_model: str
    jina_api_key: str | None = field(repr=False)
    jina_embedding_model: str
    jina_reranker_model: str
    gemini_api_key: str | None = field(repr=False)
    gemini_model: str
    jwt_secret: str | None = field(repr=False)
    approval_token_secret: str | None = field(repr=False)
    offline: bool
    llm_timeout_s: float = 60.0
    llm_max_retries: int = 2
    llm_requests_per_second: float = 2.0
    data_dir: Path = DATA_DIR
    extra_prices: dict[str, Price] = field(default_factory=dict)

    # ------------------------------------------------------------------ features
    @property
    def features(self) -> dict[str, bool]:
        """Which integrations can run. Safe to expose: booleans only, never key values."""
        online = not self.offline
        return {
            "deepseek": online and bool(self.deepseek_api_key),
            "jina": online and bool(self.jina_api_key),
            "gemini": online and bool(self.gemini_api_key),
        }

    # ------------------------------------------------------------------ models
    def model_for(self, role: str) -> str:
        """Model name for a role. Judge and reasoner use the reasoning model."""
        if role not in ROLES:
            raise ValueError(f"unknown role '{role}', expected one of {ROLES}")
        if not self.features["deepseek"]:
            return "mock"
        if role in ("judge", "reasoner"):
            return self.deepseek_reasoning_model
        return self.deepseek_model

    def price_for(self, model: str) -> Price:
        return self.extra_prices.get(model) or DEFAULT_PRICES.get(model) or UNKNOWN_PRICE


def _flag(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _secret(name: str) -> str | None:
    value = os.environ.get(name, "").strip()
    return value or None


def _extra_prices() -> dict[str, Price]:
    prices: dict[str, Price] = {}
    for key, raw in os.environ.items():
        if key.startswith("GEO_PRICE_"):
            model = key.removeprefix("GEO_PRICE_").lower().replace("_", "-")
            parts = [float(x) for x in raw.split(",")]
            if len(parts) == 3:
                prices[model] = Price(*parts)
    return prices


def load_settings(env_file: Path | None = None) -> Settings:
    """Read settings from the environment; ``.env`` never overrides variables already set."""
    load_dotenv(env_file or REPO_ROOT / ".env", override=False)
    return Settings(
        deepseek_api_key=_secret("DEEPSEEK_API_KEY"),
        deepseek_base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        deepseek_model=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"),
        deepseek_reasoning_model=os.environ.get("DEEPSEEK_REASONING_MODEL", "deepseek-reasoner"),
        jina_api_key=_secret("JINA_API_KEY"),
        jina_embedding_model=os.environ.get("JINA_EMBEDDING_MODEL", "jina-embeddings-v3"),
        jina_reranker_model=os.environ.get("JINA_RERANKER_MODEL", "jina-reranker-v2-base-multilingual"),
        gemini_api_key=_secret("GEMINI_API_KEY"),
        gemini_model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        jwt_secret=_secret("JWT_SECRET"),
        approval_token_secret=_secret("APPROVAL_TOKEN_SECRET"),
        offline=_flag("GEO_OFFLINE"),
        data_dir=Path(os.environ.get("GEO_DATA_DIR", DATA_DIR)),
        extra_prices=_extra_prices(),
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()
