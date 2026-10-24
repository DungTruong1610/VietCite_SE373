"""Site mock phải đọc được bằng công cụ trích nội dung mà Phase 2 dùng (trafilatura).

Jina Reader chạy trên máy chủ của Jina nên không đọc được localhost; ingest site mock
ở môi trường local phải đi đường fetch local + trafilatura, vì vậy test này là chuẩn.
"""

import re

import pytest

trafilatura = pytest.importorskip("trafilatura")

from .conftest import AS_OF_V1, page_paths  # noqa: E402


def h1_of(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S)
    assert m, "thiếu h1"
    return " ".join(re.sub(r"<[^>]+>", "", m.group(1)).split())


def extract(html: str) -> str:
    text = trafilatura.extract(html, include_tables=True, favor_recall=True) or ""
    return " ".join(text.split())


def test_every_page_extracts_main_content(built):
    out = built[AS_OF_V1]
    for path in page_paths(out):
        html = (
            (out / path.strip("/") / "index.html").read_text(encoding="utf-8")
            if path != "/"
            else (out / "index.html").read_text(encoding="utf-8")
        )
        text = extract(html)
        assert len(text) > 300, f"{path}: trích được quá ít chữ ({len(text)})"
        assert "Font Montserrat và Inter" not in text, f"{path}: lẫn footer"
        titles = re.findall(r'<a class="stretched" href="[^"]+">(.*?)</a>', html)
        if titles and path != "/":
            # Trang danh sách: nội dung chính là danh sách trang con, phải còn tiêu đề các mục
            assert all(t.split()[0].lower() in text.lower() for t in titles), f"{path}: mất danh sách"
        elif path != "/":
            first_words = " ".join(h1_of(html).split()[:3])
            assert first_words.lower() in text.lower(), f"{path}: mất tiêu đề"


def test_pricing_facts_survive_extraction(built):
    html = (built[AS_OF_V1] / "bang-gia" / "index.html").read_text(encoding="utf-8")
    text = extract(html)
    for needle in ("TL-START", "TL-SHOP", "TL-CHAIN", "149.000", "99.000", "399.000", "179.000"):
        assert needle in text, needle


def test_mockup_receipt_is_not_extracted_as_content(built):
    html = (built[AS_OF_V1] / "index.html").read_text(encoding="utf-8")
    text = extract(html)
    assert "Nước suối" not in text and "127.000" not in text


def test_dates_in_sentences_survive_extraction(built):
    """trafilatura bỏ nội dung thẻ <time>; ngày nằm trong câu phải là chữ thường."""
    out = built[AS_OF_V1]
    einvoice = extract((out / "tinh-nang" / "hoa-don-dien-tu" / "index.html").read_text(encoding="utf-8"))
    assert "Hiệu lực từ 01/07/2026" in einvoice and "hết hiệu lực từ 01/07/2026" in einvoice
    guide = extract(
        (out / "huong-dan" / "chuyen-tu-thue-khoan-sang-ke-khai" / "index.html").read_text(encoding="utf-8")
    )
    assert "Hiệu lực từ 01/01/2026" in guide and "17/05/2025" in guide
    pricing = extract((out / "bang-gia" / "index.html").read_text(encoding="utf-8"))
    assert "ngày 01/10/2026" in pricing and "từ 01/11/2026" in pricing
