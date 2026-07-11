from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)
from backend.assistant.models.usage import (
    Usage,
)


def test_assistant_response():

    response = AssistantResponse(
        result=RenderedResponse(
            content="Hello",
            format="markdown",
        ),
        provider="gemini",
        usage=Usage(
            total_tokens=100,
        ),
    )

    assert response.provider == "gemini"

    assert response.result.content == "Hello"

    assert response.usage.total_tokens == 100