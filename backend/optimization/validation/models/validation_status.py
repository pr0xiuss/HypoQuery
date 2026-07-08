from __future__ import annotations

from enum import Enum


class ValidationStatus(str, Enum):
    """
    Represents the outcome of validating a recommendation.
    """

    VALIDATED = "validated"

    REJECTED = "rejected"

    NOT_SUPPORTED = "not_supported"

    FAILED = "failed"