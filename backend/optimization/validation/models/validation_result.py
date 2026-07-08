from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from backend.optimization.validation.models.validation_collection import (
    ValidationCollection,
)


@dataclass(slots=True)
class ValidationResult:
    """
    Published contract of the Validation bounded context.

    Represents the complete validation outcome for one
    optimization execution.
    """

    validations: ValidationCollection = field(
        default_factory=ValidationCollection,
    )

    started_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    completed_at: datetime | None = None

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    @property
    def total_validations(self) -> int:

        return len(
            self.validations,
        )