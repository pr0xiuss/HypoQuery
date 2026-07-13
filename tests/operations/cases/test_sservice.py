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
from backend.operations.cases.repositories.memory_repository import (
    MemoryCaseRepository,
)
from backend.operations.cases.service import (
    CaseService,
)
from backend.operations.models.enums import (
    CaseIntent,
    CasePriority,
    CaseStatus,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


def build_collection() -> RecommendationReferenceCollection:
    collection = RecommendationReferenceCollection()

    collection.add(
        RecommendationReference(
            key=RecommendationKey(
                category="INDEX",
                target="orders(customer_id)",
                action="CREATE",
            ),
            recommendation_code="CREATE_INDEX",
        )
    )

    return collection


def test_service_creates_case_snapshot() -> None:
    repository = MemoryCaseRepository()

    service = CaseService(
        engine=CaseEngine(repository),
        builder=CaseBuilder(),
    )

    snapshot = service.create(
        recommendations=build_collection(),
        metadata=CaseMetadata(
            intent=CaseIntent.PERFORMANCE,
        ),
        priority=CasePriority.HIGH,
    )

    assert snapshot.priority == CasePriority.HIGH
    assert snapshot.status == CaseStatus.OPEN