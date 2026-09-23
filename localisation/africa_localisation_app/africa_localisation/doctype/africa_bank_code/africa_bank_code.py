from frappe.model.document import Document

from africa_localisation.config.banks import validate_bank_code


class AfricaBankCode(Document):
    def validate(self):
        self.code_value = validate_bank_code(self.code_type, self.code_value)

