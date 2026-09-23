# Africa Localisation for ERPNext

Shared multi-country localisation foundation for ERPNext/Frappe v15 and v16.

This app is designed for all 54 African countries. It provides:

- A single country-pack registry with ISO codes, currencies, tax authorities and
  localisation readiness.
- Stable interfaces for VAT/GST, withholding tax, payroll deductions and
  statutory reporting.
- Shared medical-aid and pension schedules, including employee and employer
  amounts.
- Shared company-contributions schedule including employer medical aid and
  employer pension.
- Version-aware helpers for ERPNext/Frappe v15 and v16.
- A country readiness matrix so incomplete or unverified regulations are visible
  instead of silently treated as production-ready.

## Important compliance boundary

The initial app is an engineering foundation, not a declaration that all 54
countries are already legally certified. Tax rates, thresholds, return layouts,
payroll bands and tax-authority APIs must be loaded from current official
notices, tested against sample returns and signed off by a local tax
professional before production use.

The existing CyteERP Zimbabwe payroll package in this workspace can be connected
as the first production country pack. The other countries start as explicit,
testable pack contracts rather than undocumented hard-coded assumptions.

## Shared payroll reports included

The shared report builders are in `africa_localisation.reports` and expose:

- `medical_aid_pension`: employee medical aid, employer medical aid, employee
  pension, employer pension, medical total, pension total and total
  contributions.
- `company_contributions`: employer social security/NSSA, employer pension,
  employer medical aid, APWCS/WCIF, employer withholding, other employer levies
  and total company contributions.

Country packs are responsible for extracting the correct Salary Slip values and
applying local statutory rules. The shared builders keep the report columns and
totals consistent across countries.

After app installation and migration, the following standard Script Reports are
available against submitted Salary Slips:

- **Africa Medical Aid and Pension**
- **Africa Company Contributions**

The default Salary Slip adapter recognises common medical-aid, health-insurance,
pension, social-security, workers-compensation and employer-levy component
names. Explicit custom fields take precedence. Production country packs should
define and test their approved component mappings.

## Install

```bash
bench get-app /path/to/africa_localisation_app
bench --site <site> install-app africa_localisation
bench --site <site> migrate
```

## Country-pack lifecycle

Each country moves through:

1. `foundation` — country metadata and extension points exist.
2. `rules_pending` — official rates, thresholds and effective dates are being
   collected and reviewed.
3. `reporting_ready` — tax/payroll calculations and statutory reports have
   passing fixtures.
4. `integration_ready` — authority e-invoicing/fiscalisation integration has
   been tested in a supported environment.
5. `production_review` — local sign-off and deployment checklist are complete.

## Planned first production wave

Zimbabwe, Zambia, Malawi, Tanzania and Kenya are the first integration wave
because the current CyteERP work already has Zimbabwe payroll/reporting assets
and these markets have clear electronic invoicing/fiscalisation interfaces.
