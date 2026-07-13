from uuid import uuid4

import pytest

from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.models.references import (
    RecommendationReference,
)
from backend.operations.verification.builders.verification_builder import (
    VerificationBuilder,
)
from backend.operations.verification.models.comparison import (
    VerificationComparison,
)
from backend.operations.verification.models.evidence import (
    VerificationEvidence,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)


def build_recommendation() -> RecommendationReference:
    return RecommendationReference(
        key=RecommendationKey(
            category="INDEX",
            target="orders(customer_id)",
            action="CREATE",
        ),
        recommendation_code="CREATE_INDEX",
    )


def test_builder_builds_verification() -> None:
    verification = (
        VerificationBuilder()
        .with_id(
            VerificationId(uuid4()),
        )
        .with_recommendation(
            build_recommendation(),
        )
        .with_comparison(
            VerificationComparison(
                expected="Index Scan",
                observed="Index Scan",
                matches=True,
            ),
        )
        .with_evidence(
            VerificationEvidence(
                execution_plan_changed=True,
                planner_changed=True,
            ),
        )
        .build()
    )

    assert verification.comparison.matches


def test_builder_requires_identifier() -> None:
    builder = (
        VerificationBuilder()
        .with_recommendation(
            build_recommendation(),
        )
        .with_comparison(
            VerificationComparison(
                expected="Index Scan",
                observed="Index Scan",
                matches=True,
            ),
        )
        .with_evidence(
            VerificationEvidence(
                execution_plan_changed=True,
                planner_changed=True,
            ),
        )
    )

    with pytest.raises(
        ValueError,
    ):
        builder.build()