from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.assistant.models.prompt import (
    Prompt,
)
from backend.assistant.providers.mock_provider import (
    MockProvider,
)


def test_mock_provider():

    provider = MockProvider()

    request = AIRequest(
        prompt=Prompt(
            system="System",
            user="User",
        )
    )

    response = provider.generate(
        request,
    )

    assert response.content == "Mock response generated."

    assert response.model == "mock"

    assert response.usage.total_tokens == 0