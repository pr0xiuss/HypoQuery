from uuid import uuid4

import pytest

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


def test_optimization_case_creation() -> None:
    case = OptimizationCase(
        id=OptimizationCaseId(uuid4()),
        recommendations=build_collection(),
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
        metadata=CaseMetadata(
            intent=CaseIntent.PERFORMANCE,
        ),
    )

    assert case.status == CaseStatus.OPEN
    assert case.priority == CasePriority.HIGH
    assert len(case.recommendations) == 1


def test_case_requires_recommendation() -> None:
    with pytest.raises(ValueError):
        OptimizationCase(
            id=OptimizationCaseId(uuid4()),
            recommendations=RecommendationReferenceCollection(),
            status=CaseStatus.OPEN,
            priority=CasePriority.MEDIUM,
            metadata=CaseMetadata(
                intent=CaseIntent.PERFORMANCE,
            ),
        )


def test_case_decisions_default_to_empty() -> None:
    case = OptimizationCase(
        id=OptimizationCaseId(uuid4()),
        recommendations=build_collection(),
        status=CaseStatus.OPEN,
        priority=CasePriority.MEDIUM,
        metadata=CaseMetadata(
            intent=CaseIntent.STABILITY,
        ),
    )

    assert case.decisions == []