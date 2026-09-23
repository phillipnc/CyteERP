# Africa country localisation matrix

The app currently registers all 54 countries as `foundation`. This is
intentional: a country must not be marked production-ready until its rates,
effective dates, return layouts, payroll rules, and integrations have been
verified against current official material.

## Integration wave

| Wave | Countries | Initial authority/integration focus |
| --- | --- | --- |
| 1 | Zimbabwe, Zambia, Malawi, Tanzania, Kenya | ZIMRA FDMS, ZRA Smart Invoice, MRA EIS, TRA EFD/VFD, KRA eTIMS; payroll and statutory reports |
| 2 | South Africa, Nigeria, Ghana, Uganda, Rwanda, Mauritius, Namibia, Botswana, Mozambique | VAT/GST, payroll, withholding tax and local e-invoicing/reporting |
| 3 | Remaining 39 countries | Country packs, official return formats, payroll rules, language/localisation and authority interfaces |

## Definition of done for a country

- Effective-dated VAT/GST, withholding and payroll rules.
- Account and tax-category mappings for a standard ERPNext chart.
- Statutory reports with export formats required by the local authority.
- Tax invoice/credit-note/debit-note print formats.
- E-invoicing or fiscalisation adapter where applicable.
- Payroll fixtures covering ordinary pay, benefits, bonuses, deductions,
  employer contributions and year-end adjustments.
- Medical-aid and pension schedules covering employee and employer amounts.
- Company-contributions schedule covering employer pension and employer medical
  aid alongside country-specific social-security and levy fields.
- Official bank directory and code data, including source references and
  effective dates where the country requires local clearing or payroll codes.
- Reconciliation tests against an approved reference workbook or return.
- Local tax review and a signed production-readiness record.
