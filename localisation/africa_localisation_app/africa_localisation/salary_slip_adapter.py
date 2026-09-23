"""Read contribution values from submitted ERPNext Salary Slips.

The adapter recognises common component names and generic custom fields.
Country packs can supply explicit custom fields or replace this adapter when a
local payroll implementation uses different component semantics.
"""

from __future__ import annotations

from typing import Any


CUSTOM_FIELDS = {
    "employee_medical": (
        "custom_employee_medical",
        "custom_medical_aid_employee",
        "custom_medical_employee",
    ),
    "employer_medical": (
        "custom_employer_medical",
        "custom_medical_aid_employer",
        "custom_medical_employer",
    ),
    "employee_pension": (
        "custom_employee_pension",
        "custom_pension_employee",
    ),
    "employer_pension": (
        "custom_employer_pension",
        "custom_pension_employer",
    ),
    "employer_nssa": (
        "custom_employer_social_security",
        "custom_social_security_employer",
        "custom_employer_nssa",
    ),
    "apwcs_wcif": (
        "custom_apwcs_wcif",
        "custom_workers_compensation_employer",
    ),
    "withholding_employer": ("custom_withholding_employer",),
    "other_employer_levies": ("custom_other_employer_levies",),
}


COMPONENT_TERMS = {
    "employee_medical": ("medical aid", "health insurance", "medical scheme"),
    "employer_medical": (
        "employer medical",
        "company medical",
        "employer health insurance",
    ),
    "employee_pension": ("employee pension", "pension", "retirement annuity"),
    "employer_pension": ("employer pension", "company pension"),
    "employer_nssa": (
        "employer social security",
        "company social security",
        "employer nssa",
        "employer nif",
    ),
    "apwcs_wcif": (
        "apwcs",
        "wcif",
        "workers compensation",
        "work injury",
    ),
    "withholding_employer": ("employer withholding",),
    "other_employer_levies": (
        "employer levy",
        "training levy",
        "skills levy",
    ),
}


def get_salary_slip_contribution_rows(filters: dict[str, Any]) -> list[dict[str, Any]]:
    import frappe

    conditions: dict[str, Any] = {"docstatus": 1}
    for field in ("company", "employee", "payroll_entry"):
        if filters.get(field):
            conditions[field] = filters[field]
    if filters.get("from_date") and filters.get("to_date"):
        conditions["posting_date"] = ["between", [filters["from_date"], filters["to_date"]]]
    if filters.get("currency"):
        conditions["currency"] = filters["currency"]

    slips = frappe.get_all(
        "Salary Slip",
        filters=conditions,
        fields=["name", "employee", "employee_name", "company", "posting_date", "currency"],
        order_by="posting_date asc, employee asc",
    )
    output: list[dict[str, Any]] = []
    for slip in slips:
        document = frappe.get_doc("Salary Slip", slip.name)
        row = {
            "employee": slip.employee,
            "employee_name": slip.employee_name,
            "company": slip.company,
            "posting_date": slip.posting_date,
            "currency": slip.currency,
        }
        for target in CUSTOM_FIELDS:
            explicit = _first_custom_value(document, CUSTOM_FIELDS[target])
            if explicit is not None:
                row[target] = explicit
                continue
            parentfield = "deductions" if target.startswith("employee_") else "earnings"
            row[target] = _component_total(document, COMPONENT_TERMS[target], parentfield)
        output.append(row)
    return output


def _first_custom_value(document: Any, fieldnames: tuple[str, ...]) -> Any | None:
    for fieldname in fieldnames:
        value = getattr(document, fieldname, None)
        if value not in (None, ""):
            return value
    return None


def _component_total(document: Any, terms: tuple[str, ...], parentfield: str) -> Any:
    total = 0
    for component in getattr(document, parentfield, ()) or ():
        haystack = _normalise(
            f"{getattr(component, 'salary_component', '')} {getattr(component, 'abbr', '')}"
        )
        if any(_normalise(term) in haystack for term in terms):
            total += getattr(component, "amount", 0) or 0
    return total


def _normalise(value: Any) -> str:
    return " ".join(str(value or "").lower().replace("_", " ").split())

