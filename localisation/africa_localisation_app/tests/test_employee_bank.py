from types import SimpleNamespace

from africa_localisation.employee_bank import allowed_bank_code_types, employee_bank_account


def test_employee_bank_payload_maps_native_and_africa_fields():
    payload = employee_bank_account(
        SimpleNamespace(
            name="EMP-001",
            employee_name="A. Employee",
            salary_mode="Bank",
            bank_name="Example Bank",
            bank_ac_no="123456",
            custom_africa_bank="BANK-00001",
            custom_africa_bank_code_type="Payroll Payment",
            custom_africa_bank_code="PAY-001",
            custom_africa_bank_branch="Main",
            custom_africa_bank_currency="ZMW",
        )
    )
    assert payload["bank_account"] == "123456"
    assert payload["africa_bank"] == "BANK-00001"
    assert payload["africa_bank_code"] == "PAY-001"


def test_employee_bank_code_types_match_bank_registry():
    assert "Payroll Payment" in allowed_bank_code_types()
    assert "SWIFT/BIC" in allowed_bank_code_types()
