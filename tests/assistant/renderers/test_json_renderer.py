import json

from backend.assistant.models.ai_response import (
    AIResponse,
)
from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.renderers.json_renderer import (
    JsonRenderer,
)


def test_json_renderer():

    renderer = JsonRenderer()

    response = AIResponse(
        content="Hello",
        model="gemini",
        usage=Usage(
            input_tokens=10,
            output_tokens=20,
            total_tokens=30,
        ),
    )

    rendered = renderer.render(
        response,
    )

    payload = json.loads(
        rendered.content,
    )

    assert payload["model"] == "gemini"

    assert payload["response"] == "Hello"

    assert (
        payload["usage"]["total_tokens"]
        == 30
    )

    assert rendered.format == "json"