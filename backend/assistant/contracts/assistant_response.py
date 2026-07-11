from __future__ import annotations

from dataclasses import dataclass

from backend.assistant.models.rendered_response import (
    RenderedResponse,
)
from backend.assistant.models.usage import (
    Usage,
)


@dataclass(
    frozen=True,
    slots=True,
)
class AssistantResponse:
    """
    Public response returned by the
    Assistant Platform.
    """

    result: RenderedResponse

    provider: str

    usage: Usage