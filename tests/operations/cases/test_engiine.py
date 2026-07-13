from uuid import uuid4

from backend.operations.cases.engine import (
    CaseEngine,
)
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
        priority=CasePriority.HIGH,
        metadata=CaseMetadata(
            intent=CaseIntent.PERFORMANCE,
        ),
    )


def test_engine_creates_case() -> None:
    repository = MemoryCaseRepository()

    engine = CaseEngine(
        repository=repository,
    )

    case = build_case()

    engine.create(case)

    assert engine.contains(case.id)


def test_engine_finds_case() -> None:
    repository = MemoryCaseRepository()

    engine = CaseEngine(
        repository=repository,
    )

    case = build_case()

    engine.create(case)

    found = engine.find(case.id)

    assert found == case


def test_engine_returns_none_for_unknown_case() -> None:
    repository = MemoryCaseRepository()

    engine = CaseEngine(
        repository=repository,
    )

    assert (
        engine.find(
            OptimizationCaseId(uuid4()),
        )
        is None
    )


def test_engine_reports_unknown_case_absence() -> None:
    repository = MemoryCaseRepository()

    engine = CaseEngine(
        repository=repository,
    )

    assert not engine.contains(
        OptimizationCaseId(uuid4()),
    )