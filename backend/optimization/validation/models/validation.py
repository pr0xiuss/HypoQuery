from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.validation.models.improvement_metrics import (
    ImprovementMetrics,
)
from backend.optimization.validation.models.validation_metadata import (
    ValidationMetadata,
)
from backend.optimization.validation.models.validation_status import (
    ValidationStatus,
)
from backend.optimization.validation.models.validation_type import (
    ValidationType,
)


@dataclass(slots=True)
class Validation:
    """
    Represents the validation outcome for a single recommendation.
    """

    recommendation: Recommendation

    status: ValidationStatus

    validation_type: ValidationType

    validation_artifact: str | None = None

    metrics: ImprovementMetrics = field(
        default_factory=ImprovementMetrics,
    )

    metadata: ValidationMetadata = field(
        default_factory=ValidationMetadata,
    )

    id: UUID = field(
        default_factory=uuid4,
    )

    validated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )