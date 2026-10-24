import json
from pathlib import Path

import pytest

from .conftest import AS_OF_V1, AS_OF_V2, REPO_BRAND, page_paths

EXPECTED_PAGES = {
    "/",
    "/tinh-nang/",
    "/tinh-nang/hoa-don-dien-tu/",
    "/tinh-nang/ban-hang-tai-quay/",
    "/bang-gia/",
    "/gioi-thieu/",
    "/huong-dan/",
    "/huong-dan/xuat-hoa-don-tu-may-tinh-tien/",
    "/huong-dan/chuyen-tu-thue-khoan-sang-ke-khai/",
    "/blog/",
    "/blog/5-viec-truoc-khi-bo-thue-khoan/",
    "/blog/ra-mat-goi-cua-hang/",
    "/hoi-dap/",
    "/chinh-sach/bao-mat/",
    "/chinh-sach/dieu-khoan-su-dung/",
    "/lien-he/",
}


def files(out: Path) -> dict[str, bytes]:
    return {p.relative_to(out).as_posix(): p.read_bytes() for p in sorted(out.rglob("*")) if p.is_file()}


def test_all_pages_and_utility_files(built):
    out = built[AS_OF_V1]
    assert set(page_paths(out)) == EXPECTED_PAGES
    for name in (
        "404.html",
        "sitemap.xml",
        "robots.txt",
        "facts.json",
        "assets/site.css",
        "assets/favicon.svg",
    ):
        assert (out / name).exists(), name
    assert not (out / "llms.txt").exists()


def test_build_is_deterministic(built, built_again):
    for as_of in (AS_OF_V1, AS_OF_V2):
        assert files(built[as_of]) == files(built_again[as_of])


@pytest.mark.parametrize("as_of", [AS_OF_V1, AS_OF_V2])
def test_committed_output_matches_fresh_build(built, as_of):
    committed = REPO_BRAND / "site" / as_of.isoformat()
    if not committed.exists():
        pytest.skip("chưa có bản build commit trong repo")
    assert files(committed) == files(built[as_of]), "Chạy lại: python -m sitegen build --all"


def test_text_files_are_precommit_clean(built):
    for out in built.values():
        for p in out.rglob("*"):
            if p.suffix in {".html", ".xml", ".txt", ".json", ".css", ".svg"}:
                text = p.read_text(encoding="utf-8")
                assert text.endswith("\n") and not text.endswith("\n\n"), p
                assert not any(line != line.rstrip() for line in text.splitlines()), p


def test_facts_json_follows_as_of(built):
    v1 = json.loads((built[AS_OF_V1] / "facts.json").read_text(encoding="utf-8"))
    v2 = json.loads((built[AS_OF_V2] / "facts.json").read_text(encoding="utf-8"))
    shop1 = next(p for p in v1["plans"] if p["code"] == "TL-SHOP")
    shop2 = next(p for p in v2["plans"] if p["code"] == "TL-SHOP")
    assert (shop1["price_month"], shop1["upcoming"]["price_month"]) == (149000, 179000)
    assert (shop2["price_month"], shop2["upcoming"]) == (179000, None)
    assert v1["is_fictional"] is True


def test_only_pricing_changes_between_versions(built):
    a, b = files(built[AS_OF_V1]), files(built[AS_OF_V2])
    changed = {k for k in a.keys() | b.keys() if a.get(k) != b.get(k)}
    assert changed == {"bang-gia/index.html", "facts.json"}


def test_price_notice_and_stale_post(built):
    v1 = (built[AS_OF_V1] / "bang-gia" / "index.html").read_text(encoding="utf-8")
    v2 = (built[AS_OF_V2] / "bang-gia" / "index.html").read_text(encoding="utf-8")
    assert "Thông báo điều chỉnh giá" in v1 and "179.000 đ" in v1 and "149.000 đ" in v1
    assert "Thông báo điều chỉnh giá" not in v2 and "149.000 đ" not in v2
    for out in built.values():
        post = (out / "blog" / "ra-mat-goi-cua-hang" / "index.html").read_text(encoding="utf-8")
        assert "129.000 đ" in post, "bài 03/2025 phải giữ giá ra mắt (bẫy D3)"


def test_sitemap_lists_every_page(built):
    sitemap = (built[AS_OF_V1] / "sitemap.xml").read_text(encoding="utf-8")
    assert sitemap.count("<loc>") == len(EXPECTED_PAGES)
    assert sitemap.count("<lastmod>") == len(EXPECTED_PAGES)
