import pytest

from africa_localisation.config.banks import (
    Bank,
    BankCode,
    get_bank,
    list_banks,
    register_bank,
    validate_bank_code,
)


def test_register_and_retrieve_country_bank_with_codes():
    bank = register_bank(
        Bank(
            country_code="ZW",
            bank_name="Example Zimbabwe Bank",
            bank_code="EXB",
            currency="ZWG",
            codes=(BankCode("SWIFT/BIC", "EXAMPLEXXXX"), BankCode("National Clearing", "1234")),
        )
    )
    assert bank.country_code == "ZW"
    assert get_bank("zw", "exb").codes[0].value == "EXAMPLEXXXX"
    assert list_banks("ZW")[0].bank_code == "EXB"


def test_swift_bic_validation():
    assert validate_bank_code("SWIFT/BIC", "ab12cd34xxx") == "AB12CD34XXX"
    with pytest.raises(ValueError):
        validate_bank_code("SWIFT/BIC", "TOO-SHORT")


def test_bank_currency_must_match_country_currency():
    with pytest.raises(ValueError):
        register_bank(
            Bank(
                country_code="KE",
                bank_name="Example Kenya Bank",
                bank_code="EXK",
                currency="USD",
            )
        )
