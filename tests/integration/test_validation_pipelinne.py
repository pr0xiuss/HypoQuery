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
from backend.assistant.validation.citation_validator import (
    CitationValidator,
)
from backend.assistant.validation.response_validator import (
    CompositeResponseValidator,
)
from backend.assistant.validation.validation_pipeline import (
    ValidationPipeline,
)


def test_full_validation_pipeline():

    validator = CompositeResponseValidator(
        ValidationPipeline(
            [
                ClaimValidator(),
                CitationValidator(),
            ]
        )
    )

    response = AssistantResponse(
        result=RenderedResponse(
            content="Optimization explanation",
            format="markdown",
        ),
        provider="gemini",
        usage=Usage(),
    )

    validator.validate(
        response,
    )