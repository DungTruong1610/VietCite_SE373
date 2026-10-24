"""Jinja2 + Markdown: filter, helper và hàm render một trang."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from datetime import date
from functools import cache
from pathlib import Path
from typing import Any

import segno
from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape
from markdown_it import MarkdownIt
from markupsafe import Markup, escape

from .content import SourcePage
from .models import Facts, LegalRef, Plan, PriceVersion

NBSP = " "
# Khung cuộn ngang cho bảng: tabindex để người dùng bàn phím cuộn được (axe: scrollable-region-focusable)
TABLE_SCROLL_OPEN = (
    '<div class="table-scroll" tabindex="0" role="region" aria-label="Bảng, cuộn ngang nếu không đủ chỗ">'
)
STATUS_LABELS = {
    "active": "Còn hiệu lực",
    "amended": "Còn hiệu lực, đã được sửa đổi",
    "superseded": "Đã bị thay thế",
    "expired": "Hết hiệu lực",
}


# ---------- filters ----------


def vnd(amount: int) -> str:
    """99000 -> '99.000 đ' (khoảng trắng không ngắt dòng)."""
    return f"{amount:,}".replace(",", ".") + f"{NBSP}đ"


def number_vi(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def date_vi(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def slugify(text: str) -> str:
    text = text.replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------- icons, QR ----------


@cache
def _icon_source(icons_dir: Path, name: str) -> str:
    path = icons_dir / f"{name}.svg"
    if not path.exists():
        raise KeyError(f"Thiếu icon {name}.svg trong {icons_dir}")
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    return re.sub(r"\s+", " ", svg).strip()


def make_icon(icons_dir: Path):
    def icon(name: str, size: int = 24, cls: str = "icon") -> Markup:
        svg = _icon_source(icons_dir, name)
        svg = re.sub(r'\s(width|height|class)="[^"]*"', "", svg)
        attrs = f'class="{cls}" width="{size}" height="{size}" aria-hidden="true" focusable="false"'
        return Markup(svg.replace("<svg", f"<svg {attrs}", 1))

    return icon


def qr_group(text: str, x: float, y: float, size: float) -> Markup:
    """Mã QR thật (quét được) dưới dạng <g> để đặt trong một SVG khác."""
    qr = segno.make(text, error="m")
    width, _ = qr.symbol_size(scale=1, border=0)
    svg = qr.svg_inline(dark="#1A1A1A", light=None, border=0, scale=1, omitsize=True)
    match = re.search(r"<svg[^>]*>(.*)</svg>", svg, flags=re.S)
    if match is None:
        raise ValueError("segno trả về SVG không đúng dạng")
    return Markup(f'<g transform="translate({x} {y}) scale({size / width:.4f})">{match.group(1)}</g>')


# ---------- context ----------


@dataclass(frozen=True)
class ResolvedPlan:
    plan: Plan
    price: PriceVersion
    upcoming: PriceVersion | None

    def __getattr__(self, name: str) -> Any:
        return getattr(self.plan, name)


@dataclass
class Site:
    facts: Facts
    as_of: date
    base_url: str
    blog_url: str
    brand_dir: Path
    pages: list[SourcePage]
    plans: dict[str, ResolvedPlan] = field(init=False)

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        self.blog_url = self.blog_url.rstrip("/") + "/"
        self.plans = {
            p.key: ResolvedPlan(p, p.price_at(self.as_of), p.upcoming_after(self.as_of))
            for p in self.facts.plans
        }

    @property
    def theme_dir(self) -> Path:
        return self.brand_dir / "theme"

    def page(self, path: str) -> SourcePage:
        for p in self.pages:
            if p.meta.path == path:
                return p
        raise KeyError(f"Không có trang {path}")

    def children(self, path: str) -> list[SourcePage]:
        kids = [p for p in self.pages if p.meta.parent == path]
        if path == "/blog/":
            return sorted(kids, key=lambda p: (p.meta.published or date.min), reverse=True)
        return kids

    def nav(self) -> list[SourcePage]:
        return [p for p in self.pages if p.meta.nav]

    def updated_of(self, page: SourcePage) -> date:
        return page.meta.updated or page.meta.published or self.facts.page_dates.default_updated

    def breadcrumbs(self, page: SourcePage) -> list[tuple[str, str]]:
        trail: list[tuple[str, str]] = []
        current: SourcePage | None = page
        while current is not None:
            label = current.meta.nav or current.meta.h1
            trail.append((label, current.meta.path))
            current = self.page(current.meta.parent) if current.meta.parent else None
        if trail[-1][1] != "/":
            trail.append(("Trang chủ", "/"))
        return list(reversed(trail))

    def url(self, path: str) -> str:
        return self.base_url + path


def law_link(ref: LegalRef, text: str | None = None) -> Markup:
    label = escape(text or ref.label)
    if ref.source_url:
        return Markup(f'<a class="law" href="{escape(ref.source_url)}">{label}</a>')
    return Markup(f'<span class="law">{label}</span>')


# ---------- markdown ----------


def _heading_ids(md: MarkdownIt) -> None:
    def rule(state) -> None:
        seen: dict[str, int] = {}
        tokens = state.tokens
        for i, tok in enumerate(tokens):
            if tok.type == "heading_open" and tok.tag in ("h2", "h3"):
                base = slugify(tokens[i + 1].content) or "muc"
                seen[base] = seen.get(base, 0) + 1
                tok.attrSet("id", base if seen[base] == 1 else f"{base}-{seen[base]}")

    md.core.ruler.push("heading_ids", rule)


def make_markdown() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table")
    _heading_ids(md)
    md.add_render_rule("table_open", lambda *a, **k: f"{TABLE_SCROLL_OPEN}<table>\n")
    md.add_render_rule("table_close", lambda *a, **k: "</table>\n</div>\n")
    return md


def extract_toc(html: str) -> list[tuple[str, str]]:
    return [
        (m.group(1), re.sub(r"<[^>]+>", "", m.group(2)))
        for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', html, flags=re.S)
    ]


# ---------- environment ----------


def make_env(site: Site) -> Environment:
    env = Environment(
        loader=FileSystemLoader(site.theme_dir / "templates"),
        autoescape=select_autoescape(["j2", "html"]),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    icons_dir = site.theme_dir / "assets" / "icons"
    env.filters.update(vnd=vnd, date_vi=date_vi, number_vi=number_vi, slugify=slugify)
    env.globals.update(
        site=site,
        facts=site.facts,
        brand=site.facts.brand,
        plans=site.plans,
        as_of=site.as_of,
        icon=make_icon(icons_dir),
        qr_group=qr_group,
        law=lambda code, text=None: law_link(site.facts.law(code), text),
        lawref=site.facts.law,
        status_label=STATUS_LABELS,
        blog_url=site.blog_url,
        table_scroll_open=Markup(TABLE_SCROLL_OPEN),
    )
    return env


def render_string(env: Environment, text: str, **ctx: Any) -> str:
    return env.from_string(text).render(**ctx)


def render_data(env: Environment, value: Any, **ctx: Any) -> Any:
    """Render Jinja trong mọi chuỗi của frontmatter `data` (để số liệu luôn lấy từ facts)."""
    if isinstance(value, str):
        return Markup(render_string(env, value, **ctx)) if "{" in value else value
    if isinstance(value, list):
        return [render_data(env, v, **ctx) for v in value]
    if isinstance(value, dict):
        return {k: render_data(env, v, **ctx) for k, v in value.items()}
    return value
