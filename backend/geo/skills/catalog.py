"""Skill catalog (ported from Buổi 4): scan ``skills/*/SKILL.md`` and keep only the metadata.

Only name, description and location go into the system prompt (progressive disclosure). The body
and references are read by the agent when a task matches the description.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

import yaml

MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024


@dataclass(frozen=True)
class SkillMeta:
    name: str
    description: str
    location: str  # relative to the workspace, e.g. skills/geo-writing/SKILL.md


@dataclass
class Catalog:
    skills: list[SkillMeta] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)

    def metadata(self) -> list[dict[str, Any]]:
        return [asdict(s) for s in self.skills]


def parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening --- frontmatter line")
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            try:
                data = yaml.safe_load("\n".join(lines[1:index]))
            except yaml.YAMLError as exc:
                raise ValueError(f"invalid YAML: {exc}") from exc
            if not isinstance(data, dict):
                raise ValueError("frontmatter must be a YAML mapping")
            return data
    raise ValueError("missing closing --- frontmatter line")


def scan_skills(workspace: Path) -> Catalog:
    catalog = Catalog()
    skills_dir = workspace / "skills"
    if not skills_dir.is_dir():
        return catalog
    seen: dict[str, str] = {}
    for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
        location = skill_file.relative_to(workspace).as_posix()
        try:
            meta = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError) as exc:
            catalog.diagnostics.append(f"skipped {location}: {exc}")
            continue
        name, description = meta.get("name"), meta.get("description")
        if not isinstance(name, str) or not name.strip():
            catalog.diagnostics.append(f"skipped {location}: missing name")
            continue
        if not isinstance(description, str) or not description.strip():
            catalog.diagnostics.append(f"skipped {location}: missing description")
            continue
        name, description = name.strip(), " ".join(description.split())
        if name in seen:
            catalog.diagnostics.append(f"error: duplicate skill '{name}' in {location}; kept {seen[name]}")
            continue
        if name != skill_file.parent.name:
            catalog.diagnostics.append(f"warning {location}: name '{name}' differs from folder name")
        if len(name) > MAX_NAME_LENGTH:
            catalog.diagnostics.append(f"warning {location}: name longer than {MAX_NAME_LENGTH} characters")
        if len(description) > MAX_DESCRIPTION_LENGTH:
            catalog.diagnostics.append(
                f"warning {location}: description longer than {MAX_DESCRIPTION_LENGTH} characters"
            )
        seen[name] = location
        catalog.skills.append(SkillMeta(name, description, location))
    return catalog


def render_catalog(catalog: Catalog) -> str:
    """``<available_skills>`` block for the system prompt; empty when there is no skill."""
    if not catalog.skills:
        return ""
    items = "\n".join(
        "  <skill>\n"
        f"    <name>{escape(s.name)}</name>\n"
        f"    <description>{escape(s.description)}</description>\n"
        f"    <location>{escape(s.location)}</location>\n"
        "  </skill>"
        for s in catalog.skills
    )
    return f"<available_skills>\n{items}\n</available_skills>"
