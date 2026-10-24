"""Build một phiên bản site (theo ngày as_of) ra fixtures/brands/<brand>/site/<as_of>/.

Build tất định: không dùng thời điểm build, duyệt file theo thứ tự cố định,
chuẩn hoá khoảng trắng cuối dòng để khớp hook pre-commit.
"""

from __future__ import annotations

import json
import os
import shutil
from datetime import date
from pathlib import Path

from .content import SourcePage, load_facts, load_pages
from .render import Site, extract_toc, make_env, make_markdown, render_data, render_string
from .seo import json_ld, robots_txt, sitemap_xml

DEMO_QR_TEXT = "Tallyo la thuong hieu gia lap phuc vu do an SE373 (UIT). Hoa don nay chi de minh hoa."


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def brand_dir(brand: str, root: Path | None = None) -> Path:
    path = (root or repo_root()) / "fixtures" / "brands" / brand
    if not (path / "content" / "facts.yaml").exists():
        raise FileNotFoundError(f"Không thấy {path / 'content' / 'facts.yaml'}")
    return path


def output_dir(bdir: Path, as_of: date) -> Path:
    return bdir / "site" / as_of.isoformat()


def normalize(text: str) -> str:
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines) + "\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(normalize(text).encode("utf-8"))


def make_site(brand: str, as_of: date, root: Path | None = None) -> Site:
    bdir = brand_dir(brand, root)
    facts = load_facts(bdir)
    cfg = facts.brand.site
    return Site(
        facts=facts,
        as_of=as_of,
        base_url=os.environ.get(cfg.base_url_env, cfg.base_url_default),
        blog_url=os.environ.get(cfg.blog_url_env, cfg.blog_url_default),
        brand_dir=bdir,
        pages=load_pages(bdir),
    )


def render_page(site: Site, env, md, page: SourcePage) -> str:
    meta = page.meta
    if meta.lede and "{" in meta.lede:
        meta = meta.model_copy(update={"lede": render_string(env, meta.lede, page=meta)})
    ctx = {"page": meta}
    body_md = render_string(env, page.body, **ctx)
    body_html = md.render(body_md)
    data = render_data(env, page.meta.data, **ctx)
    template = env.get_template(f"{page.meta.template}.html.j2")
    return template.render(
        page=meta,
        source=page,
        data=data,
        body=body_html,
        toc=extract_toc(body_html) if page.meta.toc else [],
        updated=site.updated_of(page),
        crumbs=site.breadcrumbs(page),
        json_ld=json_ld(site, page),
        canonical=site.url(page.meta.path),
        demo_qr_text=DEMO_QR_TEXT,
    )


def facts_snapshot(site: Site) -> dict:
    """Dữ kiện đã giải theo as_of: seed cho dataset D1 và đối chiếu khi kiểm tra."""
    f = site.facts
    return {
        "brand": f.brand.id,
        "as_of": site.as_of.isoformat(),
        "is_fictional": f.brand.is_fictional,
        "organization": f.brand.model_dump(mode="json", exclude={"site"}),
        "voice": f.voice.model_dump(mode="json"),
        "trial": f.trial.model_dump(mode="json"),
        "plans": [
            {
                "code": rp.code,
                "name": rp.name,
                "for_who": rp.for_who,
                "stores": rp.stores,
                "staff_accounts": rp.staff_accounts,
                "products_limit": rp.products_limit,
                "einvoice_per_year": rp.einvoice_per_year,
                "price_month": rp.price.price_month,
                "price_year": rp.price.price_year,
                "price_effective_from": rp.price.effective_from.isoformat(),
                "upcoming": rp.upcoming.model_dump(mode="json") if rp.upcoming else None,
                "extra_store_price_month": rp.extra_store_price_month,
            }
            for rp in site.plans.values()
        ],
        "addons": [a.model_dump(mode="json") for a in f.addons],
        "billing": f.billing.model_dump(mode="json"),
        "features": [x.model_dump(mode="json", exclude={"icon"}) for x in f.features],
        "compatibility": f.compatibility.model_dump(mode="json"),
        "legal": [x.model_dump(mode="json") for x in f.legal],
        "pages": [p.meta.path for p in sorted(site.pages, key=lambda p: p.meta.path)],
    }


def build(brand: str, as_of: date, root: Path | None = None) -> Path:
    site = make_site(brand, as_of, root)
    out = output_dir(site.brand_dir, as_of)
    site_root = (site.brand_dir / "site").resolve()
    if out.exists():
        if site_root not in out.resolve().parents:
            raise RuntimeError(f"Từ chối xoá thư mục ngoài {site_root}: {out}")
        shutil.rmtree(out)
    out.mkdir(parents=True)

    shutil.copytree(site.theme_dir / "assets", out / "assets", ignore=shutil.ignore_patterns("icons"))

    env = make_env(site)
    md = make_markdown()
    for page in site.pages:
        rel = page.meta.path.strip("/")
        target = out / rel / "index.html" if rel else out / "index.html"
        write(target, render_page(site, env, md, page))

    write(out / "404.html", env.get_template("404.html.j2").render(canonical=site.url("/404.html")))
    write(out / "sitemap.xml", sitemap_xml(site))
    write(out / "robots.txt", robots_txt(site))
    write(out / "facts.json", json.dumps(facts_snapshot(site), ensure_ascii=False, indent=2))
    return out
