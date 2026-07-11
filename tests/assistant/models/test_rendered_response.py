from backend.assistant.models.rendered_response import (
    RenderedResponse,
)


def test_rendered_response():

    response = RenderedResponse(
        content="# Markdown",
        format="markdown",
    )

    assert response.content == "# Markdown"

    assert response.format == "markdown"