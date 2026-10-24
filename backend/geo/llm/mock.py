"""Deterministic chat model for offline tests and CI (idea from ``MockChatModel`` in Buổi 3).

It is a real ``BaseChatModel``: ``create_agent`` calls it like an LLM and callbacks (usage, trace)
run as usual. Behaviour comes from a *policy*: a function ``messages -> AIMessage`` provided by the
agent that uses it, so each agent can script its own mock without touching this file.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langchain_core.callbacks import CallbackManagerForLLMRun
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import ConfigDict

from geo.llm.usage import CHARS_PER_TOKEN, estimate_tokens

MockPolicy = Callable[[list[BaseMessage]], AIMessage]


def tool_call(name: str, args: dict[str, Any]) -> AIMessage:
    """Helper for policies: an AIMessage that requests one tool call (id set by the model)."""
    return AIMessage(
        content="", tool_calls=[{"name": name, "args": args, "id": "pending", "type": "tool_call"}]
    )


class MockChatModel(BaseChatModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    policy: MockPolicy
    policy_name: str = "default"
    calls: int = 0

    @property
    def _llm_type(self) -> str:
        return "vietcite-mock"

    @property
    def _identifying_params(self) -> dict[str, Any]:
        return {"policy": self.policy_name}

    def bind_tools(self, tools: Any, **kwargs: Any) -> MockChatModel:  # type: ignore[override]
        return self

    def _generate(
        self,
        messages: list[BaseMessage],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs: Any,
    ) -> ChatResult:
        self.calls += 1
        msg = self.policy(messages)
        # Deterministic ids (position in the conversation) so identical runs hit the response cache.
        turn = sum(1 for m in messages if isinstance(m, AIMessage))
        msg.tool_calls = [{**c, "id": f"call_{turn}_{i}"} for i, c in enumerate(msg.tool_calls)]
        out_chars = len(str(msg.content)) + sum(len(str(c.get("args"))) for c in msg.tool_calls)
        msg.usage_metadata = {
            "input_tokens": estimate_tokens(messages),
            "output_tokens": max(1, out_chars // CHARS_PER_TOKEN),
            "total_tokens": estimate_tokens(messages) + max(1, out_chars // CHARS_PER_TOKEN),
        }
        return ChatResult(generations=[ChatGeneration(message=msg)])
