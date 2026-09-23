# Africa Localisation for ERPNext

Shared multi-country localisation foundation for ERPNext/Frappe v15 and v16.

This app is designed for all 54 African countries. It provides:

- A single country-pack registry with ISO codes, currencies, tax authorities and
  localisation readiness.
- Stable interfaces for VAT/GST, withholding tax, payroll deductions and
  statutory reporting.
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

