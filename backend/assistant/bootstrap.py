from __future__ import annotations

from backend.assistant.api.assistant_service_facade import (
    AssistantServiceFacade,
)
from backend.assistant.platform import (
    AssistantPlatform,
)
from backend.assistant.composition import (
    build_assistant_service,
)


def build_assistant_platform(
) -> AssistantPlatform:
    """
    Build the complete Assistant
    Platform.
    """

    service = build_assistant_service()

    facade = AssistantServiceFacade(
        service,
    )

    return AssistantPlatform(
        facade,
    )