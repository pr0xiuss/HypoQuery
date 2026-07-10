from backend.knowledge.models.explanation_summary import (
    ExplanationSummary,
)


def test_explanation_summary():

    summary = ExplanationSummary(
        title="Optimization Explanation",
        overview="Recommendation generated.",
        confidence=0.92,
    )

    assert (
        summary.title
        == "Optimization Explanation"
    )

    assert (
        summary.overview
        == "Recommendation generated."
    )

    assert (
        summary.confidence
        == 0.92
    )