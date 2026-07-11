from backend.assistant.api.assistant_service_facade import (
    AssistantServiceFacade,
)
from backend.assistant.assistant_context import (
    AssistantContext,
)
from backend.assistant.assistant_state.job import (
    AssistantJob,
)
from backend.assistant.contracts.assistant_request import (
    AssistantRequest,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)
from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.service import (
    AssistantService,
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


class FakeAssistantService(
    AssistantService,
):

    def __init__(self):
        pass

    def generate(
        self,
        context: AssistantContext,
        provider: str,
    ) -> RenderedResponse:

        context.response = type(
            "Response",
            (),
            {
                "usage": Usage(
                    total_tokens=42,
                )
            },
        )()

        return RenderedResponse(
            content="Hello",
            format="markdown",
        )


def test_assistant_service_facade():

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="test",
            section_count=0,
        ),
        explanation=Explanation(),
    )

    facade = AssistantServiceFacade(
        FakeAssistantService(),
    )

    response = facade.explain(
        AssistantRequest(
            explanation=snapshot,
        ),
    )

    assert response.provider == "gemini"

    assert response.result.content == "Hello"

    assert response.usage.total_tokens == 42