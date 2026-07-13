from backend.operations.outcome.models.assessment import (
    OutcomeAssessment,
)


def test_outcome_assessment() -> None:
    assessment = OutcomeAssessment(
        category="SUCCESSFUL",
        confidence=0.94,
        summary="Execution time improved significantly.",
    )

    assert assessment.category == "SUCCESSFUL"
    assert assessment.confidence == 0.94
    assert (
        assessment.summary
        == "Execution time improved significantly."
    )