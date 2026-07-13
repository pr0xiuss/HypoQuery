from __future__ import annotations

from dataclasses import dataclass, field

from backend.operations.cases.models.decision import (
    Decision,
)
from backend.operations.cases.models.metadata import (
    CaseMetadata,
)
from backend.operations.models.enums import (
    CasePriority,
    CaseStatus,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.cases.models.recommendation_reference_collection import RecommendationReferenceCollection   

@dataclass(slots=True)
class OptimizationCase:
    """
    Aggregate root representing engineering work
    undertaken to improve database performance.
    """

    id: OptimizationCaseId

    recommendations: RecommendationReferenceCollection

    status: CaseStatus

    priority: CasePriority

    metadata: CaseMetadata

    decisions: list[Decision] = field(
        default_factory=list,
    )

    def __post_init__(self) -> None:
        if len(self.recommendations) == 0:
            raise ValueError(
                "Optimization Case requires at least one recommendation."
            )