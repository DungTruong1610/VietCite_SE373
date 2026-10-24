"""Đọc facts.yaml và các trang Markdown có frontmatter YAML."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .models import Facts, PageMeta

FRONTMATTER_DELIM = "---"


@dataclass(frozen=True)
class SourcePage:
    meta: PageMeta
    body: str
    source: Path


def load_facts(brand_dir: Path) -> Facts:
    raw = yaml.safe_load((brand_dir / "content" / "facts.yaml").read_text(encoding="utf-8"))
    return Facts.model_validate(raw)


def split_frontmatter(text: str, source: Path) -> tuple[dict, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_DELIM:
        raise ValueError(f"{source}: thiếu frontmatter (dòng đầu phải là '---')")
    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == FRONTMATTER_DELIM)
    except StopIteration as exc:
        raise ValueError(f"{source}: frontmatter không có dòng '---' đóng") from exc
    meta = yaml.safe_load("\n".join(lines[1:end])) or {}
    body = "\n".join(lines[end + 1 :]).strip() + "\n"
    return meta, body


def load_pages(brand_dir: Path) -> list[SourcePage]:
    pages: list[SourcePage] = []
    content_dir = brand_dir / "content"
    for folder in ("pages", "blog"):
        for md in sorted((content_dir / folder).rglob("*.md")):
            meta, body = split_frontmatter(md.read_text(encoding="utf-8"), md)
            try:
                pages.append(SourcePage(PageMeta.model_validate(meta), body, md))
            except ValueError as exc:
                raise ValueError(f"{md}: frontmatter không hợp lệ\n{exc}") from exc
    paths = [p.meta.path for p in pages]
    duplicates = sorted({p for p in paths if paths.count(p) > 1})
    if duplicates:
        raise ValueError(f"Trùng path trang: {duplicates}")
    known = set(paths)
    for p in pages:
        if p.meta.parent and p.meta.parent not in known:
            raise ValueError(f"{p.source}: parent {p.meta.parent} không tồn tại")
    return sorted(pages, key=lambda p: (p.meta.order, p.meta.path))
