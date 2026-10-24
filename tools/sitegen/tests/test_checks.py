import pytest

from sitegen.checks import check_page, check_site
from sitegen.content import load_facts

from .conftest import AS_OF_V1, AS_OF_V2, REPO_BRAND

BASE = "http://localhost:8081"


@pytest.fixture(scope="module")
def facts():
    return load_facts(REPO_BRAND)


@pytest.mark.parametrize("as_of", [AS_OF_V1, AS_OF_V2])
def test_built_site_passes_strict_checks(built, facts, as_of):
    issues = check_site(built[as_of], facts, BASE, strict=True)
    assert [str(i) for i in issues] == []


def page(body: str, head: str = "") -> str:
    return f"""<!doctype html><html lang="vi"><head><title>Trang thử</title>
<meta name="description" content="{"x" * 130}"><meta name="robots" content="noindex">
<link rel="canonical" href="{BASE}/thu/">{head}</head>
<body><aside class="demo-notice">giả lập</aside><main><h1>Tiêu đề</h1>
<time datetime="2026-10-20">20/10/2026</time>{body}</main></body></html>"""


def rules(html: str, facts, tmp_path, strict=False) -> set[str]:
    return {i.rule for i in check_page("thu/index.html", html, tmp_path, facts, BASE, strict)}


def test_clean_page_has_no_issue(facts, tmp_path):
    assert rules(page("<h2>Mục</h2><p>Nội dung.</p>"), facts, tmp_path) == set()


@pytest.mark.parametrize(
    ("body", "rule"),
    [
        ("<h1>Thứ hai</h1>", "h1"),
        ("<h3>Nhảy cấp</h3>", "heading-order"),
        ("<p>Giá 123.000 đ mỗi tháng</p>", "vnd-not-in-facts"),
        ("<p>Rẻ hơn KiotViet</p>", "competitor"),
        ("<p>Phần mềm tốt nhất</p>", "forbidden-phrase"),
        ("<p>{{ plans.shop.name }}</p>", "placeholder"),
        ("<table><tr><td>a</td></tr></table>", "table-header"),
        ('<a href="/khong-co/">x</a>', "broken-link"),
        ('<a href="https://example.com/">x</a>', "external-link"),
        ('<img src="https://cdn.example.com/a.png">', "external-resource"),
        ("<p>Theo Nghị định 999/2099/NĐ-CP</p>", "legal-unknown"),
        (
            '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage"}</script>',
            "json-ld",
        ),
    ],
)
def test_each_rule_catches_its_defect(facts, tmp_path, body, rule):
    assert rule in rules(page(body), facts, tmp_path)


def test_price_from_facts_is_allowed(facts, tmp_path):
    assert "vnd-not-in-facts" not in rules(page("<p>Giá 149.000 đ</p>"), facts, tmp_path)


def test_svg_text_is_not_page_text(facts, tmp_path):
    html = page(
        "<svg><title>Minh hoạ dài hơn sáu mươi ký tự để thử bộ đọc tiêu đề của trang</title>"
        "<text>Tổng 127.000 đ</text></svg>"
    )
    assert rules(html, facts, tmp_path) == set()
