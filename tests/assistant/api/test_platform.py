from backend.assistant.api.assistant_facade import (
    AssistantFacade,
)
from backend.assistant.contracts.assistant_request import (
    AssistantRequest,
)
from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)
from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.platform import (
    AssistantPlatform,
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


class FakeFacade(
    AssistantFacade,
):

    def explain(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:

        return AssistantResponse(
            result=RenderedResponse(
                content="Hello",
                format="markdown",
            ),
            provider="gemini",
            usage=Usage(),
        )


def test_platform():

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="test",
            section_count=0,
        ),
        explanation=Explanation(),
    )

    platform = AssistantPlatform(
        FakeFacade(),
    )

    response = platform.explain(
        AssistantRequest(
            explanation=snapshot,
        )
    )

    assert response.provider == "gemini"

    assert response.result.content == "Hello"