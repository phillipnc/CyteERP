"""Country-neutral medical-aid, pension and company-contribution schedules.

Country packs provide the statutory rules and source Salary Slip extraction.
These builders keep the report shape consistent across countries and can be
used by Frappe Script Reports or exported to CSV/JSON by an adapter.
"""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from typing import Any, Iterable, Mapping


CENT = Decimal("0.01")
ZERO = Decimal("0.00")

COMMON_STATUTORY_REPORTS = (
    "medical_aid_pension",
    "company_contributions",
)


def money(value: Any) -> Decimal:
    if value in (None, ""):
        return ZERO
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def _value(row: Mapping[str, Any], *names: str) -> Decimal:
    for name in names:
        if name in row and row[name] not in (None, ""):
            return money(row[name])
    return ZERO


def _identity(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "employee": row.get("employee"),
        "employee_name": row.get("employee_name"),
        "company": row.get("company"),
        "posting_date": row.get("posting_date"),
        "currency": row.get("currency") or row.get("payroll_currency"),
    }


def build_medical_aid_pension(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Build the employee/employer medical-aid and pension schedule.

    The input is deliberately a mapping interface so a country adapter can
    populate it from Salary Slip, a payroll API, or a staged statutory ledger.
    """
    output: list[dict[str, Any]] = []
    totals = defaultdict(lambda: ZERO)
    for source in rows:
        row = _identity(source)
        row.update(
            {
                "employee_medical": _value(
                    source,
                    "employee_medical",
                    "medical_employee",
                    "medical_aid_employee",
                ),
                "employer_medical": _value(
                    source,
                    "employer_medical",
                    "medical_employer",
                    "medical_aid_employer",
                ),
                "employee_pension": _value(
                    source,
                    "employee_pension",
                    "pension_employee",
                ),
                "employer_pension": _value(
                    source,
                    "employer_pension",
                    "pension_employer",
                ),
            }
        )
        row["medical_total"] = row["employee_medical"] + row["employer_medical"]
        row["pension_total"] = row["employee_pension"] + row["employer_pension"]
        row["total_contributions"] = row["medical_total"] + row["pension_total"]
        output.append(row)
        for field in (
            "employee_medical",
            "employer_medical",
            "employee_pension",
            "employer_pension",
            "medical_total",
            "pension_total",
            "total_contributions",
        ):
            totals[field] += row[field]
    return {"columns": medical_aid_pension_columns(), "rows": output, "totals": dict(totals)}


def build_company_contributions(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Build a company contribution schedule including medical aid and pension."""
    output: list[dict[str, Any]] = []
    totals = defaultdict(lambda: ZERO)
    for source in rows:
        row = _identity(source)
        row.update(
            {
                "employer_nssa": _value(source, "employer_nssa", "nssa_employer"),
                "employer_pension": _value(source, "employer_pension", "pension_employer"),
                "employer_medical": _value(
                    source,
                    "employer_medical",
                    "medical_employer",
                    "medical_aid_employer",
                ),
                "apwcs_wcif": _value(source, "apwcs_wcif", "apwcs", "wcif"),
                "withholding_employer": _value(source, "withholding_employer"),
                "other_employer_levies": _value(source, "other_employer_levies"),
            }
        )
        row["total_company_contributions"] = sum(
            (
                row["employer_nssa"],
                row["employer_pension"],
                row["employer_medical"],
                row["apwcs_wcif"],
                row["withholding_employer"],
                row["other_employer_levies"],
            ),
            ZERO,
        )
        output.append(row)
        for field in (
            "employer_nssa",
            "employer_pension",
            "employer_medical",
            "apwcs_wcif",
            "withholding_employer",
            "other_employer_levies",
            "total_company_contributions",
        ):
            totals[field] += row[field]
    return {"columns": company_contributions_columns(), "rows": output, "totals": dict(totals)}


def medical_aid_pension_columns() -> list[dict[str, Any]]:
    return _columns(
        [
            ("Employee", "employee", "Link", 120),
            ("Employee Name", "employee_name", "Data", 170),
            ("Company", "company", "Link", 140),
            ("Posting Date", "posting_date", "Date", 95),
            ("Currency", "currency", "Data", 70),
            ("Employee Medical Aid", "employee_medical", "Currency", 120),
            ("Employer Medical Aid", "employer_medical", "Currency", 120),
            ("Medical Aid Total", "medical_total", "Currency", 110),
            ("Employee Pension", "employee_pension", "Currency", 115),
            ("Employer Pension", "employer_pension", "Currency", 115),
            ("Pension Total", "pension_total", "Currency", 105),
            ("Total Contributions", "total_contributions", "Currency", 125),
        ]
    )


def company_contributions_columns() -> list[dict[str, Any]]:
    return _columns(
        [
            ("Employee", "employee", "Link", 120),
            ("Employee Name", "employee_name", "Data", 170),
            ("Company", "company", "Link", 140),
            ("Posting Date", "posting_date", "Date", 95),
            ("Currency", "currency", "Data", 70),
            ("Employer NSSA/Social Security", "employer_nssa", "Currency", 145),
            ("Employer Pension", "employer_pension", "Currency", 115),
            ("Employer Medical Aid", "employer_medical", "Currency", 120),
            ("APWCS/WCIF", "apwcs_wcif", "Currency", 105),
            ("Employer Withholding", "withholding_employer", "Currency", 120),
            ("Other Employer Levies", "other_employer_levies", "Currency", 125),
            ("Total Company Contributions", "total_company_contributions", "Currency", 155),
        ]
    )


def _columns(definitions: list[tuple[str, str, str, int]]) -> list[dict[str, Any]]:
    return [
        {"label": label, "fieldname": fieldname, "fieldtype": fieldtype, "width": width}
        for label, fieldname, fieldtype, width in definitions
    ]

