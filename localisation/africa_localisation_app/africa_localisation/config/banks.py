"""Bank and bank-code primitives for country packs.

The registry intentionally ships without invented bank values. Country packs
can load bank directories from official central-bank, clearing-house or
payment-network sources and retain the source/effective date with each record.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Final

from .countries import get_country


BIC_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Z0-9]{8}([A-Z0-9]{3})?$")
CODE_TYPES: Final[tuple[str, ...]] = (
    "SWIFT/BIC",
    "National Clearing",
    "Branch",
    "Tax Payment",
    "Payroll Payment",
    "Other",
)


@dataclass(frozen=True)
class BankCode:
    code_type: str
    value: str
    branch_name: str | None = None
    active: bool = True
    source: str | None = None

    def normalised_value(self) -> str:
        return self.value.strip().upper()


@dataclass(frozen=True)
class Bank:
    country_code: str
    bank_name: str
    bank_code: str
    currency: str
    codes: tuple[BankCode, ...] = ()
    active: bool = True
    source: str | None = None


_BANKS: dict[tuple[str, str], Bank] = {}


def validate_bank_code(code_type: str, value: str) -> str:
    code_type = str(code_type or "").strip()
    normalised = str(value or "").strip().upper()
    if code_type not in CODE_TYPES:
        raise ValueError(f"Unsupported bank code type: {code_type}")
    if not normalised:
        raise ValueError("Bank code cannot be empty")
    if code_type == "SWIFT/BIC" and not BIC_RE.fullmatch(normalised):
        raise ValueError("SWIFT/BIC must contain 8 or 11 letters/numbers")
    if len(normalised) > 32:
        raise ValueError("Bank code cannot exceed 32 characters")
    return normalised


def register_bank(bank: Bank) -> Bank:
    country = get_country(bank.country_code)
    if not bank.bank_name.strip():
        raise ValueError("Bank name cannot be empty")
    if not bank.bank_code.strip():
        raise ValueError("Bank code cannot be empty")
    if bank.currency != country.currency:
        raise ValueError(
            f"{country.code} uses {country.currency}; received bank currency {bank.currency}"
        )
    validated_codes = tuple(
        BankCode(
            code_type=code.code_type,
            value=validate_bank_code(code.code_type, code.value),
            branch_name=code.branch_name,
            active=code.active,
            source=code.source,
        )
        for code in bank.codes
    )
    stored = Bank(
        country_code=country.code,
        bank_name=bank.bank_name.strip(),
        bank_code=bank.bank_code.strip().upper(),
        currency=bank.currency,
        codes=validated_codes,
        active=bank.active,
        source=bank.source,
    )
    _BANKS[(stored.country_code, stored.bank_code)] = stored
    return stored


def get_bank(country_code: str, bank_code: str) -> Bank:
    country = get_country(country_code)
    key = (country.code, str(bank_code or "").strip().upper())
    try:
        return _BANKS[key]
    except KeyError as exc:
        raise KeyError(f"Bank code not registered: {country.code}/{key[1]}") from exc


def list_banks(country_code: str | None = None, *, active_only: bool = True) -> tuple[Bank, ...]:
    country = get_country(country_code).code if country_code else None
    values = tuple(
        bank
        for bank in _BANKS.values()
        if (country is None or bank.country_code == country)
        and (not active_only or bank.active)
    )
    return tuple(sorted(values, key=lambda bank: (bank.country_code, bank.bank_name)))

