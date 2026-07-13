from uuid import uuid4

import pytest

from backend.operations.models.identifiers import (
    OutcomeId,
    VerificationId,
)
from backend.operations.outcome.builders.outcome_builder import (
    OutcomeBuilder,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.evidence import (
    OutcomeEvidence,
)
from backend.operations.outcome.models.metrics import (
    OutcomeMetrics,
)
from backend.operations.verification.models.summary import (
    VerificationSummary,
)


def build_evidence() -> OutcomeEvidence:
    return OutcomeEvidence(
        verification=VerificationSummary(
            id=VerificationId(uuid4()),
            verified=True,
        ),
        summary="Verification completed.",
    )


def test_builder_builds_outcome() -> None:
    outcome = (
        OutcomeBuilder()
        .with_id(
            OutcomeId(uuid4()),
        )
        .with_evidence(
            build_evidence(),
        )
        .with_metrics(
            OutcomeMetrics(
                performance_improvement=55.0,
                storage_overhead=3.0,
                maintenance_cost=1.0,
            ),
        )
        .with_assessment(
            OutcomeAssessment(
                category="SUCCESSFUL",
                confidence=0.95,
                summary="Optimization successful.",
            ),
        )
        .build()
    )

    assert outcome.assessment.category == "SUCCESSFUL"


def test_builder_requires_identifier() -> None:
    builder = (
        OutcomeBuilder()
        .with_evidence(
            build_evidence(),
        )
        .with_metrics(
            OutcomeMetrics(
                performance_improvement=55.0,
                storage_overhead=3.0,
                maintenance_cost=1.0,
            ),
        )
        .with_assessment(
            OutcomeAssessment(
                category="SUCCESSFUL",
                confidence=0.95,
                summary="Optimization successful.",
            ),
        )
    )

    with pytest.raises(
        ValueError,
    ):
        builder.build()