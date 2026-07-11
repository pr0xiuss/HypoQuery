import pytest

from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)
from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.validation.claim_validator import (
    ClaimValidator,
)


def test_claim_validator_accepts_content():

    response = AssistantResponse(
        result=RenderedResponse(
            content="Valid explanation",
            format="markdown",
        ),
        provider="gemini",
        usage=Usage(),
    )

    ClaimValidator().validate(
        response,
    )


def test_claim_validator_rejects_empty():

    response = AssistantResponse(
        result=RenderedResponse(
            content="   ",
            format="markdown",
        ),
        provider="gemini",
        usage=Usage(),
    )

    with pytest.raises(
        ValueError,
    ):

        ClaimValidator().validate(
            response,
        )