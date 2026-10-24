"""Bộ kiểm tra chất lượng cho site đã build (chuẩn nghiệm thu trong docs/website-tallyo/plan.html).

Mỗi lỗi là một Issue; severity "error" làm `sitegen check` trả mã thoát khác 0.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

from .models import Facts

ALLOWED_LD_TYPES = {"Organization", "WebSite", "BreadcrumbList", "ListItem", "PostalAddress"}
COMPETITORS = ("kiotviet", "sapo", "misa")
LEGAL_CODE_RE = re.compile(r"\b\d{1,4}/\d{4}/(?:NĐ-CP|TT-BTC|QH\d{2}|QĐ-TTg|QĐ-BTC)\b")
VND_RE = re.compile(r"(\d{1,3}(?:\.\d{3})+|\d+)[\s ]*(?:đ|₫|đồng|VND)(?![0-9A-Za-zÀ-ỹ])")
PLACEHOLDER_RE = re.compile(r"\{\{|\{%|\bTODO\b|lorem ipsum", re.I)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


@dataclass(frozen=True)
class Issue:
    page: str
    rule: str
    message: str
    severity: str = "error"

    def __str__(self) -> str:
        return f"[{self.severity}] {self.page} :: {self.rule} :: {self.message}"


@dataclass
class PageScan(HTMLParser):
    lang: str | None = None
    title: str = ""
    description: str | None = None
    canonical: str | None = None
    robots: str | None = None
    headings: list[tuple[int, str]] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    resources: list[str] = field(default_factory=list)
    imgs_missing_alt: int = 0
    tables: list[dict] = field(default_factory=list)
    times: list[str] = field(default_factory=list)
    ld_json: list[str] = field(default_factory=list)
    ids: list[str] = field(default_factory=list)
    has_demo_notice: bool = False
    text_parts: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        HTMLParser.__init__(self, convert_charrefs=True)
        self._stack: list[str] = []
        self._capture: str | None = None
        self._buf: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a and a["id"]:
            self.ids.append(a["id"])
        cls = (a.get("class") or "").split()
        if "demo-notice" in cls:
            self.has_demo_notice = True
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "meta" and a.get("name") == "description":
            self.description = a.get("content")
        elif tag == "meta" and a.get("name") == "robots":
            self.robots = a.get("content")
        elif tag == "link":
            if a.get("rel") == "canonical":
                self.canonical = a.get("href")
            elif a.get("href"):
                self.resources.append(a["href"])
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag in ("script", "img", "source", "iframe") and a.get("src"):
            self.resources.append(a["src"])
        if tag == "img" and not a.get("alt") and a.get("alt") != "":
            self.imgs_missing_alt += 1
        if tag == "table":
            self.tables.append({"thead": False, "th": False})
        elif tag == "thead" and self.tables:
            self.tables[-1]["thead"] = True
        elif tag == "th" and self.tables:
            self.tables[-1]["th"] = True
        elif tag == "time":
            self.times.append(a.get("datetime") or "")
        in_svg = "svg" in self._stack or tag == "svg"
        if (tag in ("h1", "h2", "h3", "h4", "h5", "h6") or (tag == "title" and not in_svg)) or (
            tag == "script" and a.get("type") == "application/ld+json"
        ):
            self._capture = "ld" if tag == "script" else tag
            self._buf = []
        if tag not in VOID:
            self._stack.append(tag)

    def handle_endtag(self, tag):
        if self._capture and (tag == self._capture or (self._capture == "ld" and tag == "script")):
            text = " ".join("".join(self._buf).split())
            if self._capture == "title":
                self.title = text
            elif self._capture == "ld":
                self.ld_json.append("".join(self._buf))
            else:
                self.headings.append((int(self._capture[1]), text))
            self._capture = None
        if self._stack and self._stack[-1] == tag:
            self._stack.pop()

    def handle_data(self, data):
        if self._capture:
            self._buf.append(data)
        if not any(t in ("script", "style", "title", "svg") for t in self._stack):
            self.text_parts.append(data)

    @property
    def text(self) -> str:
        return " ".join(" ".join(self.text_parts).split())


def scan(html: str) -> PageScan:
    s = PageScan()
    s.feed(html)
    s.close()
    return s


def _ld_types(obj) -> set[str]:
    found: set[str] = set()
    if isinstance(obj, dict):
        t = obj.get("@type")
        if isinstance(t, str):
            found.add(t)
        for v in obj.values():
            found |= _ld_types(v)
    elif isinstance(obj, list):
        for v in obj:
            found |= _ld_types(v)
    return found


def allowed_amounts(facts: Facts) -> set[int]:
    amounts: set[int] = set()
    for p in facts.plans:
        for v in p.price_history:
            amounts |= {v.price_month, v.price_year}
        if p.extra_store_price_month:
            amounts.add(p.extra_store_price_month)
    amounts |= {a.price for a in facts.addons}
    return amounts


def resolve_internal(out: Path, href: str) -> bool:
    path = href.split("#", 1)[0].split("?", 1)[0]
    if not path:
        return True
    target = out / path.lstrip("/")
    return (target / "index.html").exists() if path.endswith("/") else target.exists()


def check_page(rel: str, html: str, out: Path, facts: Facts, base_url: str, strict: bool) -> list[Issue]:
    s = scan(html)
    issues: list[Issue] = []

    def err(rule: str, msg: str, severity: str = "error") -> None:
        issues.append(Issue(rel, rule, msg, severity))

    is_404 = rel == "404.html"
    if s.lang != "vi":
        err("lang", f'<html lang> phải là "vi", đang là {s.lang!r}')
    if not s.title or len(s.title) > 60:
        err("title", f"title rỗng hoặc dài hơn 60 ký tự ({len(s.title)}): {s.title!r}")
    if not is_404 and not (s.description and 120 <= len(s.description) <= 160):
        n = len(s.description or "")
        err("meta-description", f"meta description phải 120–160 ký tự, đang {n}")
    if not (s.robots and "noindex" in s.robots):
        err("noindex", "thiếu <meta name=robots content=noindex>")
    if not s.has_demo_notice:
        err("demo-notice", "thiếu dải thông báo thương hiệu giả lập")
    if not is_404:
        expected = base_url.rstrip("/") + "/" + rel.removesuffix("index.html")
        if s.canonical != expected:
            err("canonical", f"canonical {s.canonical!r} khác {expected!r}")
    h1 = [h for h in s.headings if h[0] == 1]
    if len(h1) != 1:
        err("h1", f"phải có đúng một <h1>, đang có {len(h1)}")
    prev = 0
    for level, text in s.headings:
        if level > prev + 1:
            err("heading-order", f"heading nhảy cấp h{prev}→h{level}: {text!r}")
        prev = level
    dup_ids = sorted({i for i in s.ids if s.ids.count(i) > 1})
    if dup_ids:
        err("duplicate-id", f"id bị trùng: {dup_ids}")
    if s.imgs_missing_alt:
        err("img-alt", f"{s.imgs_missing_alt} ảnh thiếu alt")
    for i, t in enumerate(s.tables, 1):
        if not (t["thead"] and t["th"]):
            err("table-header", f"bảng thứ {i} thiếu <thead>/<th>")
    for dt in s.times:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", dt):
            err("time", f"<time datetime> không đúng dạng YYYY-MM-DD: {dt!r}")
    if not is_404 and not s.times:
        err("time", "trang không có <time datetime> nào (ngày cập nhật/đăng)")

    legal_hosts = {urlparse(x.source_url).netloc for x in facts.legal if x.source_url}
    blog_host = urlparse(facts.brand.site.blog_url_default).netloc
    for href in s.links:
        if href.startswith("/"):
            if not resolve_internal(out, href):
                err("broken-link", f"link nội bộ không tồn tại: {href}")
        elif href.startswith(("http://", "https://")):
            host = urlparse(href).netloc
            if host not in legal_hosts | {blog_host}:
                err("external-link", f"link ngoài không thuộc nguồn pháp luật hay blog: {href}")
        elif href.startswith(("mailto:", "#")):
            continue
        else:
            err("relative-link", f"dùng link gốc '/...' thay cho link tương đối: {href}")
    for res in s.resources:
        if res.startswith(("http://", "https://", "//")):
            err("external-resource", f"tài nguyên phải tự host: {res}")

    for raw in s.ld_json:
        try:
            types = _ld_types(json.loads(raw))
        except json.JSONDecodeError as exc:
            err("json-ld", f"JSON-LD không hợp lệ: {exc}")
            continue
        extra = types - ALLOWED_LD_TYPES
        if extra:
            err("json-ld", f"JSON-LD có type dành cho UC6, site gốc không được có: {sorted(extra)}")

    text = s.text
    allowed = allowed_amounts(facts)
    for m in VND_RE.finditer(text):
        amount = int(m.group(1).replace(".", ""))
        if amount not in allowed:
            err("vnd-not-in-facts", f"số tiền {m.group(0)!r} không có trong facts.yaml")
    low = text.lower()
    for phrase in facts.voice.forbidden_phrases:
        if re.search(rf"(?<![0-9A-Za-zÀ-ỹ]){re.escape(phrase.lower())}(?![0-9A-Za-zÀ-ỹ])", low):
            err("forbidden-phrase", f"có cụm từ cấm trong giọng văn: {phrase!r}")
    for name in COMPETITORS:
        if re.search(rf"\b{name}\b", low):
            err("competitor", f"nhắc tên đối thủ thật trên site Tallyo: {name}")
    if PLACEHOLDER_RE.search(text):
        err("placeholder", "còn placeholder ({{, {%, TODO, lorem)")
    known = {x.code: x for x in facts.legal}
    for code in sorted(set(LEGAL_CODE_RE.findall(text))):
        ref = known.get(code)
        if ref is None:
            err("legal-unknown", f"văn bản {code} được nhắc nhưng không có trong facts.legal")
        elif not ref.verified:
            err("legal-unverified", f"văn bản {code} chưa xác minh", "error" if strict else "warning")
    return issues


def check_site(out: Path, facts: Facts, base_url: str, strict: bool = False) -> list[Issue]:
    issues: list[Issue] = []
    html_files = sorted(out.rglob("*.html"))
    for f in html_files:
        rel = f.relative_to(out).as_posix()
        issues += check_page(rel, f.read_text(encoding="utf-8"), out, facts, base_url, strict)

    if (out / "llms.txt").exists():
        issues.append(Issue("llms.txt", "uc6-reserved", "site gốc không được có llms.txt (output của UC6)"))
    sitemap = (out / "sitemap.xml").read_text(encoding="utf-8") if (out / "sitemap.xml").exists() else ""
    pages = [f for f in html_files if f.name == "index.html"]
    for f in pages:
        path = "/" + f.parent.relative_to(out).as_posix().strip(".") + "/"
        path = path.replace("//", "/")
        loc = base_url.rstrip("/") + path
        if f"<loc>{loc}</loc>" not in sitemap:
            issues.append(Issue("sitemap.xml", "sitemap", f"thiếu {loc}"))
        if f"<loc>{loc}</loc>" in sitemap and "<lastmod>" not in sitemap:
            issues.append(Issue("sitemap.xml", "sitemap", "thiếu lastmod"))
    robots = (out / "robots.txt").read_text(encoding="utf-8") if (out / "robots.txt").exists() else ""
    if "Allow: /" not in robots or "Sitemap:" not in robots:
        issues.append(Issue("robots.txt", "robots", "robots.txt phải Allow: / và trỏ tới sitemap"))
    return issues
