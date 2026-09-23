"""Country metadata and readiness for the 54 sovereign African states.

This file deliberately contains metadata only. Tax rates and statutory rules
belong in effective-dated, reviewed country packs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class CountryDefinition:
    code: str
    name: str
    currency: str
    authority: str
    status: str = "foundation"
    e_invoicing: str | None = None
    notes: str | None = None


COUNTRIES: Final[tuple[CountryDefinition, ...]] = (
    CountryDefinition("DZ", "Algeria", "DZD", "Direction Générale des Impôts"),
    CountryDefinition("AO", "Angola", "AOA", "Administração Geral Tributária"),
    CountryDefinition("BJ", "Benin", "XOF", "Direction Générale des Impôts"),
    CountryDefinition("BW", "Botswana", "BWP", "Botswana Unified Revenue Service"),
    CountryDefinition("BF", "Burkina Faso", "XOF", "Direction Générale des Impôts"),
    CountryDefinition("BI", "Burundi", "BIF", "Office Burundais des Recettes"),
    CountryDefinition("CV", "Cabo Verde", "CVE", "Direção Nacional de Receitas do Estado"),
    CountryDefinition("CM", "Cameroon", "XAF", "Direction Générale des Impôts"),
    CountryDefinition("CF", "Central African Republic", "XAF", "Direction Générale des Impôts"),
    CountryDefinition("TD", "Chad", "XAF", "Direction Générale des Impôts"),
    CountryDefinition("KM", "Comoros", "KMF", "Administration Générale des Impôts"),
    CountryDefinition("CI", "Côte d'Ivoire", "XOF", "Direction Générale des Impôts"),
    CountryDefinition("CD", "Democratic Republic of the Congo", "CDF", "Direction Générale des Impôts"),
    CountryDefinition("DJ", "Djibouti", "DJF", "Direction Générale des Impôts"),
    CountryDefinition("EG", "Egypt", "EGP", "Egyptian Tax Authority"),
    CountryDefinition("GQ", "Equatorial Guinea", "XAF", "Dirección General de Tributos"),
    CountryDefinition("ER", "Eritrea", "ERN", "Inland Revenue Department"),
    CountryDefinition("SZ", "Eswatini", "SZL", "Eswatini Revenue Service"),
    CountryDefinition("ET", "Ethiopia", "ETB", "Ethiopian Revenue Ministry"),
    CountryDefinition("GA", "Gabon", "XAF", "Direction Générale des Impôts"),
    CountryDefinition("GM", "Gambia", "GMD", "Gambia Revenue Authority"),
    CountryDefinition("GH", "Ghana", "GHS", "Ghana Revenue Authority"),
    CountryDefinition("GN", "Guinea", "GNF", "Direction Nationale des Impôts"),
    CountryDefinition("GW", "Guinea-Bissau", "XOF", "Direção Geral das Contribuições e Impostos"),
    CountryDefinition("KE", "Kenya", "KES", "Kenya Revenue Authority", e_invoicing="KRA eTIMS"),
    CountryDefinition("LS", "Lesotho", "LSL", "Lesotho Revenue Authority"),
    CountryDefinition("LR", "Liberia", "LRD", "Liberia Revenue Authority"),
    CountryDefinition("LY", "Libya", "LYD", "Libyan Tax Administration"),
    CountryDefinition("MG", "Madagascar", "MGA", "Direction Générale des Impôts"),
    CountryDefinition("MW", "Malawi", "MWK", "Malawi Revenue Authority", e_invoicing="MRA EIS"),
    CountryDefinition("ML", "Mali", "XOF", "Direction Générale des Impôts"),
    CountryDefinition("MR", "Mauritania", "MRU", "Direction Générale des Impôts"),
    CountryDefinition("MU", "Mauritius", "MUR", "Mauritius Revenue Authority"),
    CountryDefinition("MA", "Morocco", "MAD", "Direction Générale des Impôts"),
    CountryDefinition("MZ", "Mozambique", "MZN", "Autoridade Tributária de Moçambique"),
    CountryDefinition("NA", "Namibia", "NAD", "Namibia Revenue Agency"),
    CountryDefinition("NE", "Niger", "XOF", "Direction Générale des Impôts"),
    CountryDefinition("NG", "Nigeria", "NGN", "Nigeria Revenue Service"),
    CountryDefinition("CG", "Republic of the Congo", "XAF", "Direction Générale des Impôts"),
    CountryDefinition("RW", "Rwanda", "RWF", "Rwanda Revenue Authority"),
    CountryDefinition("ST", "Sao Tome and Principe", "STN", "Direção dos Impostos"),
    CountryDefinition("SN", "Senegal", "XOF", "Direction Générale des Impôts et des Domaines"),
    CountryDefinition("SC", "Seychelles", "SCR", "Seychelles Revenue Commission"),
    CountryDefinition("SL", "Sierra Leone", "SLE", "National Revenue Authority"),
    CountryDefinition("SO", "Somalia", "SOS", "Somali Revenue Authority"),
    CountryDefinition("ZA", "South Africa", "ZAR", "South African Revenue Service"),
    CountryDefinition("SS", "South Sudan", "SSP", "National Revenue Authority"),
    CountryDefinition("SD", "Sudan", "SDG", "Sudan Taxation Chamber"),
    CountryDefinition("TZ", "Tanzania", "TZS", "Tanzania Revenue Authority", e_invoicing="TRA EFD/VFD"),
    CountryDefinition("TG", "Togo", "XOF", "Office Togolais des Recettes"),
    CountryDefinition("TN", "Tunisia", "TND", "Ministère des Finances"),
    CountryDefinition("UG", "Uganda", "UGX", "Uganda Revenue Authority"),
    CountryDefinition("ZM", "Zambia", "ZMW", "Zambia Revenue Authority", e_invoicing="ZRA Smart Invoice"),
    CountryDefinition("ZW", "Zimbabwe", "ZWG", "Zimbabwe Revenue Authority", e_invoicing="ZIMRA FDMS"),
)

BY_CODE: Final[dict[str, CountryDefinition]] = {country.code: country for country in COUNTRIES}


def get_country(code: str) -> CountryDefinition:
    """Return a country definition using an ISO alpha-2 code."""
    normalised = str(code or "").strip().upper()
    try:
        return BY_CODE[normalised]
    except KeyError as exc:
        raise ValueError(f"Unsupported African country code: {normalised}") from exc


def supported_country_codes() -> tuple[str, ...]:
    return tuple(country.code for country in COUNTRIES)

