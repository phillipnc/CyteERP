import frappe
from frappe.model.document import Document

from africa_localisation.config.banks import get_country, validate_bank_code


class AfricaBank(Document):
    def validate(self):
        country = get_country(self.country_code)
        if self.currency != country.currency:
            frappe.throw(
                f"{country.name} uses {country.currency}; "
                "the bank currency must match the country currency."
            )
        if self.swift_bic:
            self.swift_bic = validate_bank_code("SWIFT/BIC", self.swift_bic)

