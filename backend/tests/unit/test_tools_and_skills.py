from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

from geo.skills.catalog import render_catalog, scan_skills
from geo.tools.calculator import CALCULATE, calculate, format_vi
from geo.tools.registry import ToolRegistry, ToolSpec


# ------------------------------------------------------------------ calculator
def test_calculate_exact_and_formats_vietnamese():
    r = calculate("2400000*30*0.015")
    assert r["status"] == "ok" and r["result"] == 1080000.0 and r["result_vi"] == "1.080.000"
    assert format_vi(__import__("decimal").Decimal("1234.5")) == "1.234,5"


def test_calculate_rejects_code_and_bad_input():
    assert calculate("__import__('os').system('dir')")["error"] == "invalid_expression"
    assert calculate("1/0")["error"] == "division_by_zero"
    assert calculate("2**1000")["error"] == "invalid_expression"
    assert calculate("1+" * 200)["error"] == "expression_too_long"


# ------------------------------------------------------------------ registry
class _Args(BaseModel):
    x: int


def _boom(x: int) -> dict:
    raise RuntimeError("bug in tool")


def test_registry_validates_and_wraps_tool_exceptions():
    reg = ToolRegistry([CALCULATE, ToolSpec("boom", "fails", _Args, _boom)])
    assert reg.validate_call("nope", {})["error"] == "unknown_tool"
    assert reg.validate_call("boom", {"x": "abc"})["error"] == "schema_violation"
    assert reg.validate_call("calculate", {"expression": "1+1", "extra": 1})["status"] == "invalid_param"
    assert reg.execute("boom", {"x": 1})["error"] == "tool_exception"
    tools = reg.langchain_tools(["calculate"])
    assert [t.name for t in tools] == ["calculate"]


# ------------------------------------------------------------------ skill catalog
def test_skill_catalog_progressive_disclosure(tmp_path: Path):
    good = tmp_path / "skills" / "geo-writing"
    good.mkdir(parents=True)
    (good / "SKILL.md").write_text(
        "---\nname: geo-writing\ndescription: Viết bài GEO tiếng Việt.\n---\nBody\n", encoding="utf-8"
    )
    bad = tmp_path / "skills" / "broken"
    bad.mkdir()
    (bad / "SKILL.md").write_text("no frontmatter", encoding="utf-8")
    catalog = scan_skills(tmp_path)
    assert [s.name for s in catalog.skills] == ["geo-writing"]
    assert any("broken" in d for d in catalog.diagnostics)
    block = render_catalog(catalog)
    assert "<available_skills>" in block and "Body" not in block
