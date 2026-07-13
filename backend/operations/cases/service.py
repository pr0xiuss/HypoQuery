from __future__ import annotations

from uuid import uuid4

from backend.operations.cases.builders.case_builder import (
    CaseBuilder,
)
from backend.operations.cases.engine import (
    CaseEngine,
)
from backend.operations.cases.models.metadata import (
    CaseMetadata,
)
from backend.operations.cases.models.recommendation_reference_collection import (
    RecommendationReferenceCollection,
)
from backend.operations.contracts.snapshots import (
    OptimizationCaseSnapshot,
)
from backend.operations.models.enums import (
    CasePriority,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)


class CaseService:
    """
    Application service for
    Optimization Case operations.
    """

    def __init__(
        self,
        engine: CaseEngine,
        builder: CaseBuilder,
    ) -> None:
        self._engine = engine
        self._builder = builder

    def create(
        self,
        *,
        recommendations: RecommendationReferenceCollection,
        metadata: CaseMetadata,
        priority: CasePriority,
    ) -> OptimizationCaseSnapshot:

        case = (
            self._builder
            .with_id(
                OptimizationCaseId(
                    uuid4(),
                )
            )
            .with_recommendations(
                recommendations,
            )
            .with_metadata(
                metadata,
            )
            .with_priority(
                priority,
            )
            .build()
        )

        self._engine.create(
            case,
        )

        return OptimizationCaseSnapshot(
            case_id=case.id,
            status=case.status,
            priority=case.priority,
        )