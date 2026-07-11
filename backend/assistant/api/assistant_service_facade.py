from __future__ import annotations

from backend.assistant.api.assistant_facade import (
    AssistantFacade,
)
from backend.assistant.assistant_context import (
    AssistantContext,
)
from backend.assistant.assistant_state.job import (
    AssistantJob,
)
from backend.assistant.contracts.assistant_request import (
    AssistantRequest,
)
from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.service import (
    AssistantService,
)


class AssistantServiceFacade(
    AssistantFacade,
):
    """
    Default facade implementation backed
    by AssistantService.
    """

    def __init__(
        self,
        service: AssistantService,
    ) -> None:

        self._service = service

    def explain(
        self,
        request: AssistantRequest,
    ) -> AssistantResponse:

        context = AssistantContext(
            job=AssistantJob(
                explanation=request.explanation,
            )
        )

        rendered = self._service.generate(
            context=context,
            provider=request.provider,
        )

        return AssistantResponse(
            result=rendered,
            provider=request.provider,
            usage=context.response.usage,
        )