"""LLM gateway: the single place that builds chat models.

Every model it returns already has:
- the model chosen for its *role* (``Settings.model_for``) or the mock when offline / no key;
- timeout, retries with backoff (``max_retries``) and a client-side rate limiter;
- the shared response cache (SQLite) when one is given;
- a ``UsageCallback`` that counts tokens, prompt-cache hits and cost into the run's ``Usage``.

DeepSeek's chat model runs with thinking disabled for tool-calling and extraction roles: thinking
mode refuses forced ``tool_choice`` and structured output (finding from Buổi 3).
"""

from __future__ import annotations

from langchain_core.caches import BaseCache
from langchain_core.language_models import BaseChatModel
from langchain_core.rate_limiters import InMemoryRateLimiter

from geo.config import Settings
from geo.llm.mock import MockChatModel, MockPolicy
from geo.llm.usage import Usage, UsageCallback


class LLMUnavailableError(RuntimeError):
    """Raised when a real model is required but the key is missing or offline mode is on."""


class LLMGateway:
    def __init__(self, settings: Settings, usage: Usage, cache: BaseCache | None = None) -> None:
        self.settings, self.usage, self.cache = settings, usage, cache
        self._limiter = InMemoryRateLimiter(
            requests_per_second=settings.llm_requests_per_second,
            check_every_n_seconds=0.05,
            max_bucket_size=max(1, int(settings.llm_requests_per_second)),
        )

    def chat_model(
        self,
        role: str,
        *,
        mock_policy: MockPolicy | None = None,
        mock_name: str = "default",
        force_mock: bool = False,
        require_real: bool = False,
    ) -> BaseChatModel:
        name = "mock" if force_mock else self.settings.model_for(role)
        if name == "mock":
            if require_real:
                raise LLMUnavailableError(
                    "DeepSeek is not available: set DEEPSEEK_API_KEY and GEO_OFFLINE=false"
                )
            if mock_policy is None:
                raise ValueError(f"role '{role}' runs on the mock model but no mock_policy was given")
            callback = UsageCallback(self.usage, self.settings.price_for("mock"), "mock", role)
            return MockChatModel(
                policy=mock_policy, policy_name=mock_name, cache=self.cache, callbacks=[callback]
            )

        from langchain_openai import ChatOpenAI

        thinking_off = name != self.settings.deepseek_reasoning_model
        callback = UsageCallback(self.usage, self.settings.price_for(name), name, role)
        return ChatOpenAI(
            model=name,
            api_key=self.settings.deepseek_api_key,  # type: ignore[arg-type]
            base_url=self.settings.deepseek_base_url,
            temperature=0,
            timeout=self.settings.llm_timeout_s,
            max_retries=self.settings.llm_max_retries,
            rate_limiter=self._limiter,
            extra_body={"thinking": {"type": "disabled"}} if thinking_off else None,
            cache=self.cache,
            callbacks=[callback],
        )
