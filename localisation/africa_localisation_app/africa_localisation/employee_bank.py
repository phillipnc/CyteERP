"""ERPNext Employee bank-account integration.

ERPNext v15/v16 stores the primary employee payment account on Employee
(`bank_name`, `bank_ac_no`, and salary mode). These helpers add an optional
Africa Bank link and validated country-specific payment code without replacing
the native fields.
"""

from __future__ import annotations

from typing import Any

from .config.banks import CODE_TYPES, validate_bank_code


def validate_employee_bank(doc: Any, method: str | None = None) -> None:
    """Validate and enrich an Employee document during save."""
    africa_bank = getattr(doc, "custom_africa_bank", None)
    if not africa_bank:
        return

    import frappe

    bank = frappe.db.get_value(
        "Africa Bank",
        africa_bank,
        ["bank_name", "country_code", "currency", "bank_code", "active"],
        as_dict=True,
    )
    if not bank:
        frappe.throw(f"Africa Bank {africa_bank} was not found.")
    if not bank.active:
        frappe.throw(f"Africa Bank {africa_bank} is inactive.")

    code_type = getattr(doc, "custom_africa_bank_code_type", None)
    code_value = getattr(doc, "custom_africa_bank_code", None)
    if code_value:
        try:
            normalised = validate_bank_code(code_type or "Other", code_value)
        except ValueError as exc:
            frappe.throw(str(exc))
        doc.custom_africa_bank_code = normalised
    elif code_type:
        frappe.throw("Africa bank code type requires an Africa bank code.")

    # Keep standard ERPNext payroll/bank-remittance consumers populated.
    if not getattr(doc, "bank_name", None):
        doc.bank_name = bank.bank_name
    doc.custom_africa_bank_currency = bank.currency


def employee_bank_account(doc: Any) -> dict[str, Any]:
    """Return a normalised employee bank-account payload for payroll adapters."""
    return {
        "employee": getattr(doc, "name", None),
        "employee_name": getattr(doc, "employee_name", None),
        "salary_mode": getattr(doc, "salary_mode", None),
        "bank_name": getattr(doc, "bank_name", None),
        "bank_account": getattr(doc, "bank_ac_no", None),
        "africa_bank": getattr(doc, "custom_africa_bank", None),
        "africa_bank_code_type": getattr(doc, "custom_africa_bank_code_type", None),
        "africa_bank_code": getattr(doc, "custom_africa_bank_code", None),
        "africa_bank_branch": getattr(doc, "custom_africa_bank_branch", None),
        "currency": getattr(doc, "custom_africa_bank_currency", None),
    }


def allowed_bank_code_types() -> tuple[str, ...]:
    return CODE_TYPES

