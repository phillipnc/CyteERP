"""Country-pack registry.

The registry keeps metadata and implementation selection separate. This lets us
install all 54 country definitions without pretending every rule set is already
legally reviewed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from africa_localisation.config.countries import CountryDefinition, get_country


@dataclass(frozen=True)
class PackRegistration:
    country: CountryDefinition
    implementation: Any | None = None
    reviewed: bool = False


_PACKS: dict[str, PackRegistration] = {}


def register_pack(country_code: str, implementation: Any, *, reviewed: bool = False) -> None:
    country = get_country(country_code)
    _PACKS[country.code] = PackRegistration(country, implementation, reviewed)


def get_pack(country_code: str) -> PackRegistration:
    country = get_country(country_code)
    return _PACKS.get(country.code, PackRegistration(country))


def readiness_matrix() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for code in sorted({registration.country.code for registration in _PACKS.values()} | set(_all_codes())):
        registration = _PACKS.get(code)
        country = registration.country if registration else get_country(code)
        rows.append(
            {
                "country_code": country.code,
                "country": country.name,
                "authority": country.authority,
                "currency": country.currency,
                "status": "reviewed" if registration and registration.reviewed else country.status,
                "e_invoicing": country.e_invoicing,
                "pack_loaded": bool(registration and registration.implementation),
            }
        )
    return rows


def _all_codes() -> tuple[str, ...]:
    from africa_localisation.config.countries import supported_country_codes

    return supported_country_codes()

