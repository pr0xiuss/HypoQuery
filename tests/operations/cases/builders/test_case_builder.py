from uuid import uuid4

import pytest

from backend.operations.cases.builders.case_builder import (
    CaseBuilder,
)
from backend.operations.cases.models.metadata import (
    CaseMetadata,
)
from backend.operations.cases.models.recommendation_reference_collection import (
    RecommendationReferenceCollection,
)
from backend.operations.models.enums import (
    CaseIntent,
    CasePriority,
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


def test_builder_creates_case() -> None:
    case = (
        CaseBuilder()
        .with_id(
            OptimizationCaseId(
                uuid4(),
            )
        )
        .with_recommendations(
            build_collection(),
        )
        .with_metadata(
            CaseMetadata(
                intent=CaseIntent.PERFORMANCE,
            )
        )
        .with_priority(
            CasePriority.HIGH,
        )
        .build()
    )

    assert case.priority == CasePriority.HIGH
    assert len(case.recommendations) == 1


def test_builder_requires_identifier() -> None:
    with pytest.raises(ValueError):
        (
            CaseBuilder()
            .with_recommendations(
                build_collection(),
            )
            .with_metadata(
                CaseMetadata(
                    intent=CaseIntent.PERFORMANCE,
                )
            )
            .build()
        )


def test_builder_requires_recommendations() -> None:
    with pytest.raises(ValueError):
        (
            CaseBuilder()
            .with_id(
                OptimizationCaseId(
                    uuid4(),
                )
            )
            .with_metadata(
                CaseMetadata(
                    intent=CaseIntent.PERFORMANCE,
                )
            )
            .build()
        )


def test_builder_requires_metadata() -> None:
    with pytest.raises(ValueError):
        (
            CaseBuilder()
            .with_id(
                OptimizationCaseId(
                    uuid4(),
                )
            )
            .with_recommendations(
                build_collection(),
            )
            .build()
        )