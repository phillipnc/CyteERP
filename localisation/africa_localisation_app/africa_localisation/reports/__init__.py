"""Shared statutory report builders for Africa country packs."""

from .contributions import (
    COMMON_STATUTORY_REPORTS,
    build_company_contributions,
    build_medical_aid_pension,
)

__all__ = [
    "COMMON_STATUTORY_REPORTS",
    "build_company_contributions",
    "build_medical_aid_pension",
]

