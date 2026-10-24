"""Cache-friendly prompt layout (Buổi 7): static prefix first, dynamic suffix last.

The provider's prompt cache only reuses a prefix that is byte-for-byte identical. So:
- the **system message** holds only what never changes within a role: instructions, skill catalog,
  rules. ``assert_static`` rejects timestamps and run ids there, because one changed character
  near the start invalidates the cache for everything after it;
- everything that changes per run (brand data, evidence, the request) goes into the **last**
  human message, wrapped in tags.
"""

from __future__ import annotations

import re
from collections.abc import Mapping

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

VOLATILE = [
    (re.compile(r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}"), "timestamp"),
    (re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"), "uuid"),
    (re.compile(r"\brun_[0-9a-f]{8,}\b"), "run id"),
]


class VolatilePrefixError(ValueError):
    """The static prefix contains something that changes between runs."""


def assert_static(text: str) -> None:
    for pattern, label in VOLATILE:
        m = pattern.search(text)
        if m:
            raise VolatilePrefixError(
                f"static prefix contains a {label} ('{m.group(0)}'); move it to the suffix"
            )


def build_system_prompt(*sections: str) -> str:
    """Join the static sections of a role's system prompt; empty sections are skipped."""
    text = "\n\n".join(s.strip() for s in sections if s and s.strip())
    assert_static(text)
    return text


def build_user_message(request: str, context: Mapping[str, str] | None = None) -> HumanMessage:
    """Dynamic suffix: per-run context blocks, then the request itself."""
    blocks = [f"<{name}>\n{value.strip()}\n</{name}>" for name, value in (context or {}).items() if value]
    blocks.append(f"<request>\n{request.strip()}\n</request>")
    return HumanMessage(content="\n\n".join(blocks))


def build_messages(
    system_prompt: str, request: str, context: Mapping[str, str] | None = None
) -> list[BaseMessage]:
    assert_static(system_prompt)
    return [SystemMessage(content=system_prompt), build_user_message(request, context)]
