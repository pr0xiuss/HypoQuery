from __future__ import annotations

from dataclasses import dataclass, field

from backend.assistant.assistant_state.job import (
    AssistantJob,
)
from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.assistant.models.ai_response import (
    AIResponse,
)


@dataclass(slots=True)
class AssistantContext:
    """
    Mutable context shared across the assistant
    generation pipeline.
    """

    job: AssistantJob

    request: AIRequest | None = field(
        default=None,
    )

    response: AIResponse | None = field(
        default=None,
    )