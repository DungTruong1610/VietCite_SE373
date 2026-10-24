"""Tool registry: allowlist + argument schema + LangChain packaging (ported from Buổi 3).

The two syntactic checks live here:
    1. unknown tool          → only names registered here exist
    2. bad argument format   → Pydantic validation before the function runs
Semantic checks (permission, grounding) live in ``geo.harness``.

A tool function returns a dict with an explicit ``status`` (see ``geo.harness.contract``). An
exception inside a tool becomes an ``error`` envelope instead of crashing the agent.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ValidationError

from geo.harness.contract import error


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    args_schema: type[BaseModel]
    func: Callable[..., dict[str, Any]]
    side_effect: bool = False  # changes the world (write, publish, pay)
    polling: bool = False  # calling again to wait for a state change is legitimate


class ToolRegistry:
    def __init__(self, specs: Iterable[ToolSpec]) -> None:
        self.specs: dict[str, ToolSpec] = {}
        for spec in specs:
            if spec.name in self.specs:
                raise ValueError(f"duplicate tool '{spec.name}'")
            self.specs[spec.name] = spec

    @property
    def write_tools(self) -> frozenset[str]:
        return frozenset(n for n, s in self.specs.items() if s.side_effect)

    @property
    def polling_tools(self) -> frozenset[str]:
        return frozenset(n for n, s in self.specs.items() if s.polling)

    def validate_call(self, name: str, args: dict[str, Any]) -> dict[str, Any] | None:
        """Structured error observation if the call is invalid, else None."""
        spec = self.specs.get(name)
        if spec is None:
            return {
                "status": "denied",
                "error": "unknown_tool",
                "tool": name,
                "hint": f"Only these tools exist: {sorted(self.specs)}",
            }
        try:
            spec.args_schema.model_validate(args)
        except ValidationError as exc:
            first = exc.errors()[0]
            return {
                "status": "invalid_param",
                "error": "schema_violation",
                "param": ".".join(str(p) for p in first["loc"]),
                "detail": first["msg"],
                "hint": f"Arguments must match the schema of {name}",
            }
        return None

    def execute(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        spec = self.specs[name]
        clean = spec.args_schema.model_validate(args).model_dump(exclude_none=True)
        try:
            return spec.func(**clean)
        except Exception as exc:  # a tool bug must not crash the agent loop
            return error("tool_exception", f"{type(exc).__name__}: {exc}", retryable=False)

    def langchain_tools(self, names: Iterable[str] | None = None) -> list[Any]:
        """``StructuredTool`` objects for ``create_agent`` / ``bind_tools``."""
        from langchain_core.tools import StructuredTool

        def make(spec: ToolSpec) -> StructuredTool:
            def _run(**kwargs: Any) -> dict[str, Any]:
                return self.execute(spec.name, kwargs)

            return StructuredTool.from_function(
                func=_run, name=spec.name, description=spec.description, args_schema=spec.args_schema
            )

        wanted = list(names) if names is not None else list(self.specs)
        return [make(self.specs[n]) for n in wanted if n in self.specs]
