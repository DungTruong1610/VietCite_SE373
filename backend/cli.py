"""Command line: ``uv run geo <command>`` from ``backend/``.

    geo hello  [--mode mock|live] [--question "..."]   run the Phase 1 hello agent, print trace + usage
    geo trace  <file.jsonl> [--locate]                 print a trace or its first bad event
    geo smoke                                          call each real provider once (skips missing keys)

Output never contains key values.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer

from geo.config import get_settings

app = typer.Typer(add_completion=False, help="VietCite Studio command line")
DEFAULT_QUESTION = (
    "Một shop bán 2.400.000đ mỗi ngày. 30 ngày thì doanh thu bao nhiêu, và 1,5% của số đó là bao nhiêu?"
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]


@app.command()
def hello(
    mode: Annotated[str, typer.Option(help="mock or live (DeepSeek)")] = "mock",
    question: Annotated[str, typer.Option(help="question for the calculator agent")] = DEFAULT_QUESTION,
) -> None:
    """Run the hello agent (create_agent + HarnessMiddleware + calculate tool)."""
    from geo.agents.hello import run_hello

    if mode not in ("mock", "live"):
        raise typer.BadParameter("mode must be mock or live")
    result = run_hello(question, mode=mode)  # type: ignore[arg-type]
    for event in result.events:
        typer.echo(event.line())
    typer.echo("-" * 78)
    typer.echo(f"model      : {result.model}")
    typer.echo(f"stop       : {result.stop_reason} · {result.detail}")
    typer.echo(f"answer     : {result.answer}")
    typer.echo(f"usage      : {result.usage}")
    typer.echo(f"trace file : {result.trace_file}")
    raise typer.Exit(0 if result.stop_reason == "GOAL" else 1)


@app.command()
def trace(path: Path, locate: Annotated[bool, typer.Option(help="only the first bad event")] = False) -> None:
    """Print a trace JSONL file (step 2 of the debug process: locate the first bad step)."""
    from geo.tracing.trace import main

    raise typer.Exit(main([str(path)] + (["--locate"] if locate else [])))


@app.command()
def smoke() -> None:
    """Call each configured provider once. PASS / SKIP (no key) / FAIL, never prints keys."""
    from geo.providers.jina import JinaClient

    s = get_settings()
    failures = 0

    def report(name: str, status: str, detail: str = "") -> None:
        nonlocal failures
        failures += status == "FAIL"
        typer.echo(f"{status:<5} {name:<22} {detail}")

    def attempt(name: str, func) -> None:
        try:
            report(name, "PASS", func())
        except Exception as exc:  # report and continue with the next provider
            report(name, "FAIL", f"{type(exc).__name__}: {str(exc)[:160]}")

    if s.features["deepseek"]:
        from geo.agents.hello import run_hello

        def deepseek() -> str:
            r = run_hello(DEFAULT_QUESTION, mode="live", use_cache=False)
            if r.stop_reason != "GOAL":
                raise RuntimeError(f"{r.stop_reason}: {r.detail}")
            u = r.usage
            return (
                f"{r.model} · {u['model_calls']} calls · {u['tokens_in']}+{u['tokens_out']} tokens · "
                f"cached {u['cached_tokens']} · ${u['cost_usd']:.5f}"
            )

        attempt("deepseek hello agent", deepseek)
    else:
        report("deepseek hello agent", "SKIP", "DEEPSEEK_API_KEY missing or GEO_OFFLINE=true")

    if s.features["jina"]:
        jina = JinaClient(s.jina_api_key or "", s.jina_embedding_model, s.jina_reranker_model)
        attempt(
            "jina embeddings",
            lambda: f"dim={len(jina.embed(['phần mềm bán hàng'], task='retrieval.query')[0])}",
        )
        attempt(
            "jina rerank",
            lambda: (
                "top="
                + str(
                    jina.rerank("hoá đơn điện tử", ["giá cà phê", "xuất hoá đơn điện tử"], top_n=1)[0].index
                )
            ),
        )
        attempt("jina reader", lambda: f"{len(jina.read('https://example.com').content)} chars")
        attempt("jina search", lambda: f"{len(jina.search('phần mềm quản lý bán hàng', limit=3))} hits")
        typer.echo(f"      jina tokens used: {jina.tokens_used}")
        jina.close()
    else:
        report("jina", "SKIP", "JINA_API_KEY missing or GEO_OFFLINE=true")

    if s.features["gemini"]:
        from geo.providers.gemini_probe import GeminiProbe

        def gemini() -> str:
            r = GeminiProbe(s.gemini_api_key or "", s.gemini_model).probe(
                "Phần mềm bán hàng cho hộ kinh doanh?"
            )
            return f"{s.gemini_model} · {len(r.sources)} sources · {len(r.text)} chars"

        attempt("gemini grounding", gemini)
    else:
        report("gemini grounding", "SKIP", "GEMINI_API_KEY missing")

    raise typer.Exit(1 if failures else 0)


if __name__ == "__main__":
    app()
