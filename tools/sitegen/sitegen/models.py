"""Mô hình dữ liệu của facts.yaml và frontmatter trang.

Mọi model dùng extra="forbid" để gõ sai tên trường là báo lỗi ngay lúc build.
"""

from __future__ import annotations

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Customers(Strict):
    count: int
    as_of: date
    wording: str
    source_page: str


class Contact(Strict):
    support_email: str
    sales_email: str
    support_hours: str
    phone: str | None = None


class SiteConfig(Strict):
    base_url_env: str
    base_url_default: str
    blog_url_env: str
    blog_url_default: str


class Brand(Strict):
    id: str
    name: str
    is_fictional: bool
    aliases: list[str]
    legal_name: str
    category: str
    tagline: str
    founded_year: int
    city: str
    team_size: int
    customers: Customers
    mission: str
    audience: list[str]
    usp: list[str]
    contact: Contact
    site: SiteConfig


class Voice(Strict):
    formality: str
    self_reference: str
    address_reader: str
    sentence_style: str
    sample_sentences: list[str]
    forbidden_phrases: list[str]
    required_terms: list[str]
    notes: str


class Trial(Strict):
    days: int
    credit_card_required: bool
    included_plan: str
    data_kept_days: int
    source_page: str


class PriceVersion(Strict):
    effective_from: date
    price_month: int
    price_year: int


class Plan(Strict):
    code: str
    key: str
    name: str
    for_who: str
    stores: int
    staff_accounts: int
    products_limit: int | None
    einvoice_per_year: int
    highlighted: bool = False
    extra_store_price_month: int | None = None
    price_history: list[PriceVersion] = Field(min_length=1)

    @model_validator(mode="after")
    def _history_sorted(self) -> Plan:
        dates = [p.effective_from for p in self.price_history]
        if dates != sorted(dates) or len(set(dates)) != len(dates):
            raise ValueError(
                f"{self.code}: price_history phải tăng dần theo effective_from, không trùng ngày"
            )
        return self

    def price_at(self, as_of: date) -> PriceVersion:
        """Bản giá đang hiệu lực tại ngày as_of."""
        current = [p for p in self.price_history if p.effective_from <= as_of]
        if not current:
            raise ValueError(f"{self.code}: chưa có giá hiệu lực tại {as_of}")
        return current[-1]

    def upcoming_after(self, as_of: date) -> PriceVersion | None:
        """Bản giá đã công bố nhưng chưa hiệu lực tại ngày as_of (nếu có)."""
        future = [p for p in self.price_history if p.effective_from > as_of]
        return future[0] if future else None


class Addon(Strict):
    key: str
    name: str
    price: int
    validity_months: int


class Refund(Strict):
    annual_first_payment_days: int
    monthly_refundable: bool
    einvoice_issued_refundable: bool
    source_page: str


class Billing(Strict):
    year_discount_note: str
    price_change_notice_days: int
    price_change_announced_on: date
    price_change_rule: str
    refund: Refund
    payment_methods: list[str]


class Feature(Strict):
    key: str
    name: str
    summary: str
    plans: list[str]
    page: str
    icon: str


class Compatibility(Strict):
    platforms: list[str]
    printers: list[str]
    printer_connections: list[str]
    scanners: list[str]
    sells_hardware: bool
    offline_mode: str
    source_page: str


LegalStatus = Literal["active", "amended", "superseded", "expired"]


class LegalRef(Strict):
    code: str
    kind: str
    title: str
    issuer: str
    signed_date: date | None = None
    effective_date: date
    ended_on: date | None = None
    status: LegalStatus
    point: str
    article: str | None = None
    quote: str | None = None
    amended_by: list[str] = Field(default_factory=list)
    superseded_by: str | None = None
    source_url: str | None
    verified: bool
    verified_on: date | None = None
    note: str | None = None

    @model_validator(mode="after")
    def _verified_has_source(self) -> LegalRef:
        if self.verified and not (self.source_url and self.verified_on):
            raise ValueError(f"{self.code}: verified=true phải có source_url và verified_on")
        if self.status in ("superseded", "expired") and not self.ended_on:
            raise ValueError(f"{self.code}: văn bản hết hiệu lực phải có ended_on")
        return self

    @property
    def label(self) -> str:
        return f"{self.kind} {self.code}"


class Guides(Strict):
    einvoice_setup_minutes: int


class LegalFacts(Strict):
    threshold_label: str
    old_threshold_label: str
    einvoice_register_days: int
    revenue_notice_deadline: str
    quarterly_deadline: str
    monthly_deadline: str
    books_retention_years: int
    registration_form: str
    verified_on: date


class Privacy(Strict):
    data_location: str
    retention_after_cancel_years: int


class PageDates(Strict):
    default_updated: date
    blog: dict[str, date]


class BuildSpec(Strict):
    as_of: date
    note: str


class Facts(Strict):
    schema_version: int
    brand: Brand
    voice: Voice
    trial: Trial
    plans: list[Plan]
    addons: list[Addon]
    billing: Billing
    features: list[Feature]
    compatibility: Compatibility
    legal: list[LegalRef]
    legal_refs: dict[str, str]
    legal_facts: LegalFacts
    guides: Guides
    privacy: Privacy
    page_dates: PageDates
    builds: list[BuildSpec]

    @model_validator(mode="after")
    def _unique_keys(self) -> Facts:
        for name, items in (("plans", [p.code for p in self.plans]), ("legal", [x.code for x in self.legal])):
            if len(items) != len(set(items)):
                raise ValueError(f"{name}: có mã bị trùng")
        codes = {p.code for p in self.plans}
        for f in self.features:
            unknown = set(f.plans) - codes
            if unknown:
                raise ValueError(f"feature {f.key}: gói không tồn tại {sorted(unknown)}")
        legal_codes = {x.code for x in self.legal}
        missing = {k: v for k, v in self.legal_refs.items() if v not in legal_codes}
        if missing:
            raise ValueError(f"legal_refs trỏ tới văn bản không có trong legal: {missing}")
        if self.trial.included_plan not in codes:
            raise ValueError("trial.included_plan không phải mã gói hợp lệ")
        return self

    def plan(self, key_or_code: str) -> Plan:
        for p in self.plans:
            if key_or_code in (p.key, p.code):
                return p
        raise KeyError(key_or_code)

    def law(self, code: str) -> LegalRef:
        for x in self.legal:
            if x.code == code:
                return x
        raise KeyError(f"Không có văn bản {code} trong facts.legal")


PageTemplate = Literal["home", "pricing", "doc", "index", "faq", "contact"]


class PageMeta(Strict):
    """Frontmatter của một file Markdown trong content/pages hoặc content/blog."""

    path: str
    title: str
    description: str
    template: PageTemplate
    h1: str
    eyebrow: str | None = None
    lede: str | None = None
    nav: str | None = None
    parent: str | None = None
    summary: str | None = None
    icon: str | None = None
    order: int = 100
    updated: date | None = None
    published: date | None = None
    toc: bool = False
    cta: bool = True
    listing: str | None = None
    laws: list[str] = Field(default_factory=list)
    data: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _path_shape(self) -> PageMeta:
        if not (self.path.startswith("/") and self.path.endswith("/")):
            raise ValueError(f"path phải bắt đầu và kết thúc bằng '/': {self.path}")
        return self
