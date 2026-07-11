from backend.assistant.contracts.assistant_request import (
    AssistantRequest,
)
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_metadata import (
    ExplanationMetadata,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


def test_assistant_request():

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="test",
            section_count=0,
        ),
        explanation=Explanation(),
    )

    request = AssistantRequest(
        explanation=snapshot,
    )

    assert request.explanation == snapshot

    assert request.provider == "gemini"

    assert request.renderer == "markdown"

    assert request.audience == "developer"