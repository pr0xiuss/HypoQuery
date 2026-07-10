from unittest.mock import MagicMock
from unittest.mock import patch

from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.assistant.models.prompt import (
    Prompt,
)
from backend.assistant.providers.gemini_provider import (
    GeminiProvider,
)


@patch(
    "backend.assistant.providers.gemini_provider.genai.Client",
)
def test_gemini_provider(
    mock_client,
):

    usage = MagicMock()

    usage.prompt_token_count = 10

    usage.candidates_token_count = 20

    usage.total_token_count = 30

    response = MagicMock()

    response.text = "Hello"

    response.usage_metadata = usage

    client = MagicMock()

    client.models.generate_content.return_value = (
        response
    )

    mock_client.return_value = client

    provider = GeminiProvider()

    result = provider.generate(
        AIRequest(
            prompt=Prompt(
                system="System",
                user="User",
            ),
        ),
    )

    assert result.content == "Hello"

    assert result.model is not None

    assert result.usage.total_tokens == 30