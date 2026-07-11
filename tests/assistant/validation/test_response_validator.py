from backend.assistant.contracts.assistant_response import (
    AssistantResponse,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)
from backend.assistant.models.usage import (
    Usage,
)
from backend.assistant.validation.base_validator import (
    ResponseValidator,
)
from backend.assistant.validation.response_validator import (
    CompositeResponseValidator,
)
from backend.assistant.validation.validation_pipeline import (
    ValidationPipeline,
)


class FakeValidator(
    ResponseValidator,
):

    def __init__(
        self,
    ) -> None:

        self.called = False

    def validate(
        self,
        response: AssistantResponse,
    ) -> None:

        self.called = True


def test_response_validator():

    validator = FakeValidator()

    response_validator = (
        CompositeResponseValidator(
            ValidationPipeline(
                [validator],
            )
        )
    )

    response = AssistantResponse(
        result=RenderedResponse(
            content="Hello",
            format="markdown",
        ),
        provider="gemini",
        usage=Usage(),
    )

    response_validator.validate(
        response,
    )

    assert validator.called