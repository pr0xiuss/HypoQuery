from backend.assistant.factories.renderer_factory import (
    RendererFactory,
)
from backend.assistant.renderers.json_renderer import (
    JsonRenderer,
)
from backend.assistant.renderers.markdown_renderer import (
    MarkdownRenderer,
)


def test_renderer_factory():

    factory = RendererFactory()

    markdown = factory.create(
        "markdown",
    )

    json = factory.create(
        "json",
    )

    assert isinstance(
        markdown,
        MarkdownRenderer,
    )

    assert isinstance(
        json,
        JsonRenderer,
    )