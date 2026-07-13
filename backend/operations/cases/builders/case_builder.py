from __future__ import annotations

from backend.operations.cases.models.metadata import (
    CaseMetadata,
)
from backend.operations.cases.models.optimization_case import (
    OptimizationCase,
)
from backend.operations.cases.models.recommendation_reference_collection import (
    RecommendationReferenceCollection,
)
from backend.operations.models.enums import (
    CasePriority,
    CaseStatus,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)


class CaseBuilder:
    """
    Fluent builder for constructing
    Optimization Case aggregates.
    """

    def __init__(self) -> None:
        self._id: OptimizationCaseId | None = None
        self._recommendations: (
            RecommendationReferenceCollection | None
        ) = None
        self._metadata: CaseMetadata | None = None
        self._priority: CasePriority = CasePriority.MEDIUM
        self._status: CaseStatus = CaseStatus.OPEN

    def with_id(
        self,
        identifier: OptimizationCaseId,
    ) -> "CaseBuilder":
        self._id = identifier
        return self

    def with_recommendations(
        self,
        recommendations: RecommendationReferenceCollection,
    ) -> "CaseBuilder":
        self._recommendations = recommendations
        return self

    def with_metadata(
        self,
        metadata: CaseMetadata,
    ) -> "CaseBuilder":
        self._metadata = metadata
        return self

    def with_priority(
        self,
        priority: CasePriority,
    ) -> "CaseBuilder":
        self._priority = priority
        return self

    def with_status(
        self,
        status: CaseStatus,
    ) -> "CaseBuilder":
        self._status = status
        return self

    def build(self) -> OptimizationCase:
        if self._id is None:
            raise ValueError(
                "Optimization Case identifier is required."
            )

        if self._recommendations is None:
            raise ValueError(
                "Recommendation collection is required."
            )

        if self._metadata is None:
            raise ValueError(
                "Case metadata is required."
            )
        
        if len(self._recommendations) == 0:
            raise ValueError(
                "At least one recommendation is required."
            )

        return OptimizationCase(
            id=self._id,
            recommendations=self._recommendations,
            status=self._status,
            priority=self._priority,
            metadata=self._metadata,
        )