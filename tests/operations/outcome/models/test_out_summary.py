from uuid import uuid4

from backend.operations.models.identifiers import (
    OutcomeId,
)
from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)
from backend.operations.outcome.models.summary import (
    OutcomeSummary,
)


def test_outcome_summary() -> None:
    summary = OutcomeSummary(
        id=OutcomeId(uuid4()),
        assessment=OutcomeAssessment(
            category="SUCCESSFUL",
            confidence=0.90,
            summary="Assessment completed.",
        ),
    )

    assert summary.assessment.category == "SUCCESSFUL"