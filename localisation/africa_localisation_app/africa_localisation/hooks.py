app_name = "africa_localisation"
app_title = "Africa Localisation"
app_publisher = "CyteERP Systems"
app_description = "Multi-country Africa tax, payroll and statutory localisation foundation"
app_email = "support@cyteerp.com"
app_license = "MIT"

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Employee-custom_africa_bank",
                    "Employee-custom_africa_bank_code_type",
                    "Employee-custom_africa_bank_code",
                    "Employee-custom_africa_bank_branch",
                    "Employee-custom_africa_bank_currency",
                ],
            ]
        ],
    }
]

doc_events = {
    "Employee": {
        "validate": "africa_localisation.employee_bank.validate_employee_bank",
    }
}
