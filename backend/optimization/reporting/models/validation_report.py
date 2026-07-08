from __future__ import annotations
from dataclasses import dataclass
from backend.optimization.validation.models.validation_status import ValidationStatus
from backend.optimization.validation.models.validation_type import ValidationType

@dataclass(slots=True)
class ValidationReport:
    """
    Human-readable validation summary.
    """

    status: ValidationStatus | None

    validation_type: ValidationType | None

    improvement_percent: float

    cost_before: float

    cost_after: float

    plan_changed: bool