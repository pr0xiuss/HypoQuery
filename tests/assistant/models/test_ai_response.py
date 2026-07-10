from backend.assistant.models.ai_response import (
    AIResponse,
)
from backend.assistant.models.usage import (
    Usage,
)


def test_ai_response():

    usage = Usage(
        input_tokens=100,
        output_tokens=50,
        total_tokens=150,
    )

    response = AIResponse(
        content="Hello",
        model="gemini",
        usage=usage,
    )

    assert response.content == "Hello"

    assert response.model == "gemini"

    assert response.usage == usage