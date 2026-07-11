from backend.assistant.composition import (
    build_assistant_service,
)
from backend.assistant.service import (
    AssistantService,
)


def test_build_assistant_service():

    service = build_assistant_service()

    assert isinstance(
        service,
        AssistantService,
    )