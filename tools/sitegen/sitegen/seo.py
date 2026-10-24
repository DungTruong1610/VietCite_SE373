"""sitemap.xml, robots.txt và JSON-LD ở mức tối thiểu.

Cố ý KHÔNG sinh llms.txt, FAQPage, HowTo, SoftwareApplication: đó là output của UC6,
site gốc không có để thí nghiệm đo được phần đóng góp của UC6.
"""

from __future__ import annotations

import json
from xml.sax.saxutils import escape

from markupsafe import Markup

from .content import SourcePage
from .render import Site


def sitemap_xml(site: Site) -> str:
    rows = []
    for page in sorted(site.pages, key=lambda p: p.meta.path):
        rows.append(
            "  <url>\n"
            f"    <loc>{escape(site.url(page.meta.path))}</loc>\n"
            f"    <lastmod>{site.updated_of(page).isoformat()}</lastmod>\n"
            "  </url>"
        )
    body = "\n".join(rows)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n</urlset>\n"
    )


def robots_txt(site: Site) -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {site.url('/sitemap.xml')}\n"


def _organization(site: Site) -> dict:
    b = site.facts.brand
    return {
        "@type": "Organization",
        "@id": site.url("/#organization"),
        "name": b.name,
        "legalName": b.legal_name,
        "url": site.url("/"),
        "email": b.contact.support_email,
        "foundingDate": str(b.founded_year),
        "address": {"@type": "PostalAddress", "addressLocality": b.city, "addressCountry": "VN"},
        "description": f"{b.category}. Thương hiệu giả lập phục vụ đồ án SE373 (UIT).",
    }


def json_ld(site: Site, page: SourcePage) -> Markup:
    if page.meta.path == "/":
        graph = [
            _organization(site),
            {
                "@type": "WebSite",
                "@id": site.url("/#website"),
                "name": site.facts.brand.name,
                "url": site.url("/"),
                "inLanguage": "vi",
                "publisher": {"@id": site.url("/#organization")},
            },
        ]
    else:
        graph = [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": i, "name": name, "item": site.url(path)}
                    for i, (name, path) in enumerate(site.breadcrumbs(page), start=1)
                ],
            }
        ]
    data = {"@context": "https://schema.org", "@graph": graph}
    text = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    return Markup(f'<script type="application/ld+json">\n{text}\n</script>')
