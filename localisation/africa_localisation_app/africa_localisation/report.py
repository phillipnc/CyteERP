"""Frappe-independent report metadata shared by country adapters."""

from __future__ import annotations

from .reports.contributions import COMMON_STATUTORY_REPORTS


def statutory_report_codes() -> tuple[str, ...]:
    """Return report codes that every production country pack may expose."""
    return COMMON_STATUTORY_REPORTS

