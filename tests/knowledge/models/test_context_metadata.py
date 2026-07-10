from backend.knowledge.models.context_metadata import (
    ContextMetadata,
)


def test_context_metadata():

    metadata = ContextMetadata(
        objective="find_recommendations",
        evidence_count=4,
        section_count=2,
    )

    assert (
        metadata.objective
        == "find_recommendations"
    )

    assert (
        metadata.evidence_count
        == 4
    )

    assert (
        metadata.section_count
        == 2
    )