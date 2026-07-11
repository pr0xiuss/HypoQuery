from backend.knowledge.models.explanation_metadata import (
    ExplanationMetadata,
)


def test_explanation_metadata():

    metadata = ExplanationMetadata(
        objective="find_recommendations",
        section_count=3,
    )

    assert (
        metadata.objective
        == "find_recommendations"
    )

    assert (
        metadata.section_count
        == 3
    )