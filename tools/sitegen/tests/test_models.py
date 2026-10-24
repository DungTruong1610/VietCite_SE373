from datetime import date

import pytest
from pydantic import ValidationError

from sitegen.content import load_facts
from sitegen.models import Facts, LegalRef, PageMeta
from sitegen.render import date_vi, number_vi, slugify, vnd

from .conftest import AS_OF_V1, AS_OF_V2, REPO_BRAND


@pytest.fixture(scope="module")
def facts() -> Facts:
    return load_facts(REPO_BRAND)


def test_filters():
    assert vnd(149000) == "149.000 đ"
    assert vnd(1490000) == "1.490.000 đ"
    assert number_vi(10000) == "10.000"
    assert date_vi(date(2026, 11, 1)) == "01/11/2026"


@pytest.mark.parametrize(
    ("text", "slug"),
    [
        ("Sổ sách hộ kinh doanh", "so-sach-ho-kinh-doanh"),
        ("Hoá đơn điện tử", "hoa-don-dien-tu"),
        ("Căn cứ pháp lý", "can-cu-phap-ly"),
        ("Đơn online", "don-online"),
    ],
)
def test_slugify_vietnamese(text, slug):
    assert slugify(text) == slug


def test_price_resolution_by_date(facts):
    shop = facts.plan("TL-SHOP")
    assert shop.price_at(date(2025, 3, 1)).price_month == 129000
    assert shop.price_at(AS_OF_V1).price_month == 149000
    assert shop.upcoming_after(AS_OF_V1).price_month == 179000
    assert shop.price_at(AS_OF_V2).price_month == 179000
    assert shop.upcoming_after(AS_OF_V2) is None
    with pytest.raises(ValueError):
        shop.price_at(date(2024, 1, 1))


def test_year_price_is_ten_months(facts):
    for plan in facts.plans:
        for version in plan.price_history:
            assert version.price_year == version.price_month * 10, plan.code


def test_legal_refs_point_to_known_documents(facts):
    codes = {x.code for x in facts.legal}
    assert set(facts.legal_refs.values()) <= codes


def test_unknown_plan_in_feature_is_rejected(facts):
    raw = facts.model_dump()
    raw["features"][0]["plans"] = ["TL-KHONG-CO"]
    with pytest.raises(ValidationError, match="gói không tồn tại"):
        Facts.model_validate(raw)


def test_verified_law_needs_source():
    with pytest.raises(ValidationError, match="verified=true"):
        LegalRef(
            code="1/2026/NĐ-CP",
            kind="Nghị định",
            title="x",
            issuer="Chính phủ",
            effective_date=date(2026, 1, 1),
            status="active",
            point="x",
            source_url=None,
            verified=True,
        )


def test_page_path_shape():
    with pytest.raises(ValidationError):
        PageMeta(path="bang-gia", title="t", description="d", template="doc", h1="h")
