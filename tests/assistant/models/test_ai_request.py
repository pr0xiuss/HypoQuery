from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.assistant.models.prompt import (
    Prompt,
)


def test_ai_request():

    prompt = Prompt(
        system="System",
        user="User",
    )

    request = AIRequest(
        prompt=prompt,
    )

    assert request.prompt == prompt

    assert request.temperature == 0.2

    assert request.max_tokens == 1024