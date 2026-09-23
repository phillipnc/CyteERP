"""Small compatibility surface for ERPNext/Frappe v15 and v16."""

from __future__ import annotations

from typing import Any


def frappe_version() -> tuple[int, int] | None:
    try:
        import frappe
    except ImportError:
        return None
    version = getattr(frappe, "__version__", "")
    parts = str(version).split(".")
    try:
        return int(parts[0]), int(parts[1])
    except (IndexError, TypeError, ValueError):
        return None


def is_supported_frappe(version: tuple[int, int] | None = None) -> bool:
    current = version or frappe_version()
    return current is None or current[0] in (15, 16)


def get_report_filters(filters: Any) -> dict[str, Any]:
    if filters is None:
        return {}
    if isinstance(filters, dict):
        return filters
    if hasattr(filters, "as_dict"):
        return filters.as_dict()
    return dict(filters)

