from africa_localisation.reports import build_company_contributions
from africa_localisation.salary_slip_adapter import get_salary_slip_contribution_rows


def execute(filters=None):
    result = build_company_contributions(get_salary_slip_contribution_rows(filters or {}))
    return result["columns"], result["rows"]

