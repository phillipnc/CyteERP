from decimal import Decimal

from africa_localisation.reports import build_company_contributions, build_medical_aid_pension


def test_medical_aid_and_pension_schedule_includes_employee_and_employer_values():
    result = build_medical_aid_pension(
        [
            {
                "employee": "EMP-001",
                "employee_name": "A. Employee",
                "currency": "ZMW",
                "employee_medical": "20",
                "employer_medical": "80",
                "employee_pension": "45",
                "employer_pension": "45",
            }
        ]
    )
    row = result["rows"][0]
    assert row["medical_total"] == Decimal("100.00")
    assert row["pension_total"] == Decimal("90.00")
    assert row["total_contributions"] == Decimal("190.00")
    assert result["totals"]["employer_medical"] == Decimal("80.00")
    assert result["totals"]["employer_pension"] == Decimal("45.00")


def test_company_contributions_includes_medical_aid_and_pension():
    result = build_company_contributions(
        [
            {
                "employee": "EMP-001",
                "employer_nssa": 30,
                "employer_medical": 80,
                "employer_pension": 45,
                "apwcs_wcif": 5,
            }
        ]
    )
    row = result["rows"][0]
    assert row["total_company_contributions"] == Decimal("160.00")
    assert result["totals"]["employer_medical"] == Decimal("80.00")
    assert result["totals"]["employer_pension"] == Decimal("45.00")

