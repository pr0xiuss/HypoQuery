from uuid import uuid4

from backend.operations.cases.models.metadata import (
    CaseMetadata,
)
from backend.operations.cases.models.optimization_case import (
    OptimizationCase,
)
from backend.operations.cases.models.recommendation_reference_collection import (
    RecommendationReferenceCollection,
)
from backend.operations.cases.repositories.memory_repository import (
    MemoryCaseRepository,
)
from backend.operations.models.enums import (
    CaseIntent,
    CasePriority,
    CaseStatus,
)
from backend.operations.models.identifiers import (
    OptimizationCaseId,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


def build_case() -> OptimizationCase:
    recommendations = RecommendationReferenceCollection()

    recommendations.add(
        RecommendationReference(
            key=RecommendationKey(
                category="INDEX",
                target="orders(customer_id)",
                action="CREATE",
            ),
            recommendation_code="CREATE_INDEX",
        )
    )

    return OptimizationCase(
        id=OptimizationCaseId(uuid4()),
        recommendations=recommendations,
        status=CaseStatus.OPEN,
        priority=CasePriority.MEDIUM,
        metadata=CaseMetadata(
            intent=CaseIntent.PERFORMANCE,
        ),
    )


def test_add_case() -> None:
    repository = MemoryCaseRepository()

    case = build_case()

    repository.add(case)

    assert repository.contains(case.id)


def test_find_case() -> None:
    repository = MemoryCaseRepository()

    case = build_case()

    repository.add(case)

    assert repository.find(case.id) == case


def test_find_unknown_case_returns_none() -> None:
    repository = MemoryCaseRepository()

    assert (
        repository.find(
            OptimizationCaseId(uuid4()),
        )
        is None
    )


def test_contains_unknown_case_returns_false() -> None:
    repository = MemoryCaseRepository()

    assert not repository.contains(
        OptimizationCaseId(uuid4()),
    )