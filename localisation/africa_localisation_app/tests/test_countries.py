from africa_localisation.config.countries import COUNTRIES, get_country
from africa_localisation.core.registry import readiness_matrix


def test_registry_contains_54_african_countries():
    assert len(COUNTRIES) == 54
    assert len({country.code for country in COUNTRIES}) == 54


def test_known_country_metadata():
    assert get_country("zw").currency == "ZWG"
    assert get_country("ke").e_invoicing == "KRA eTIMS"
    assert get_country("zm").authority == "Zambia Revenue Authority"


def test_readiness_matrix_is_explicit_for_every_country():
    rows = readiness_matrix()
    assert len(rows) == 54
    assert {row["country_code"] for row in rows} == {country.code for country in COUNTRIES}
    assert all(row["pack_loaded"] is False for row in rows)

