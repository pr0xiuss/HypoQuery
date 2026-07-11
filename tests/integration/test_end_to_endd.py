from backend.assistant.bootstrap import (
    build_assistant_platform,
)
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


def test_end_to_end():

    platform = build_assistant_platform()

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="integration",
            section_count=0,
        ),
        explanation=Explanation(),
    )

    request = AssistantRequest(
        explanation=snapshot,
        provider="mock",
    )

    response = platform.explain(
        request,
    )

    assert response.provider == "mock"

    assert response.result.content == "Mock response generated."