"""Stable contracts implemented by country localisation packs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any, Protocol


@dataclass(frozen=True)
class EffectiveDate:
    start: date
    end: date | None = None

    def contains(self, value: date) -> bool:
        return value >= self.start and (self.end is None or value <= self.end)


@dataclass(frozen=True)
class TaxRule:
    code: str
    label: str
    tax_type: str
    rate: Decimal | None
    effective: EffectiveDate
    recoverable: bool = False
    notes: str | None = None


@dataclass(frozen=True)
class PayrollRule:
    code: str
    label: str
    side: str
    basis: str
    rate: Decimal | None
    ceiling: Decimal | None
    effective: EffectiveDate
    notes: str | None = None


@dataclass
class StatutoryReportResult:
    report_code: str
    country_code: str
    period_start: date
    period_end: date
    columns: list[dict[str, Any]] = field(default_factory=list)
    rows: list[dict[str, Any]] = field(default_factory=list)
    totals: dict[str, Decimal] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


class CountryPack(Protocol):
    country_code: str

    def tax_rules(self, as_at: date) -> list[TaxRule]:
        ...

    def payroll_rules(self, as_at: date) -> list[PayrollRule]:
        ...

    def statutory_reports(self) -> tuple[str, ...]:
        ...

