"""Numeric grounding: every number in an answer must come from a source (generalised from Buổi 3).

Sources are plain text: the user's request plus the tool observations (later: the Evidence
Ledger). A number is grounded when the same value appears in a source, whatever the notation:
Vietnamese ``2.400.000`` / ``1,5`` and JSON ``2400000.0`` / ``1.5`` are compared as values.

Phase 5 extends this to dates, document numbers (``70/2025/NĐ-CP``), prices and names.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

# A number starts and ends with a digit and may contain '.' or ',' inside (2.400.000 · 1,5 · 72000000.0).
# Units glued after it (2.400.000đ, 15%) are fine; letters before it (V2, B01) are not numbers.
NUMBER = re.compile(r"(?<![\w.,])\d(?:[\d.,]*\d)?(?!\d)")
VI_THOUSANDS = re.compile(r"^\d{1,3}(\.\d{3})+(,\d+)?$")
EN_THOUSANDS = re.compile(r"^\d{1,3}(,\d{3})+(\.\d+)?$")


def parse_number(token: str) -> Decimal | None:
    """Parse one numeric token in Vietnamese or English/JSON notation."""
    t = token.strip().rstrip(".,")
    try:
        if VI_THOUSANDS.match(t):
            return Decimal(t.replace(".", "").replace(",", "."))
        if EN_THOUSANDS.match(t):
            return Decimal(t.replace(",", ""))
        if "," in t and "." not in t:
            return Decimal(t.replace(",", "."))
        return Decimal(t)
    except InvalidOperation:
        return None


def extract_numbers(text: str) -> list[tuple[str, Decimal]]:
    """(token as written, value) in order of appearance, without duplicates."""
    seen: list[tuple[str, Decimal]] = []
    for m in NUMBER.finditer(text):
        value = parse_number(m.group(0))
        if value is not None and all(v != value for _, v in seen):
            seen.append((m.group(0), value))
    return seen


def _matches(value: Decimal, sources: list[Decimal]) -> bool:
    for s in sources:
        if s == value:
            return True
        if s != 0 and abs(s - value) <= max(Decimal("0.5"), abs(s) * Decimal("1e-9")) and abs(value) >= 10:
            return True  # rounding of large amounts (1080000.0000001 vs 1.080.000)
    return False


@dataclass
class GroundingReport:
    ok: bool
    grounded: list[str] = field(default_factory=list)
    ungrounded: list[str] = field(default_factory=list)

    def render(self) -> str:
        rows = [f"grounded    {g}" for g in self.grounded]
        rows += [f"UNGROUNDED  {u}" for u in self.ungrounded]
        return "\n".join(rows)


def check_numbers(answer: str, sources: list[str]) -> GroundingReport:
    source_values = [v for text in sources for _, v in extract_numbers(text)]
    rep = GroundingReport(ok=True)
    for token, value in extract_numbers(answer):
        (rep.grounded if _matches(value, source_values) else rep.ungrounded).append(token)
    rep.ok = not rep.ungrounded
    return rep
