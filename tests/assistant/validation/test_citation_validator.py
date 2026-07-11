from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)
from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.validation.citation_validator import (
    CitationValidator,
)


def test_citation_validator():

    response = AssistantResponse(
        result=RenderedResponse(
            content="Explanation",
            format="markdown",
        ),
        provider="gemini",
        usage=Usage(),
    )

    CitationValidator().validate(
        response,
    )