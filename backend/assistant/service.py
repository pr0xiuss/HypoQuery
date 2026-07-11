from __future__ import annotations

from backend.assistant.assistant_context import (
    AssistantContext,
)
from backend.assistant.engine import (
    AssistantEngine,
)
from backend.assistant.models.rendered_response import (
    RenderedResponse,
)
from backend.assistant.prompts.base_prompt_builder import (
    PromptBuilder,
)
from backend.assistant.renderers.markdown_renderer import (
    MarkdownRenderer,
)


class AssistantService:
    """
    Application service responsible for executing the
    assistant pipeline.
    """

    def __init__(
        self,
        prompt_builder: PromptBuilder,
        engine: AssistantEngine,
        renderer: MarkdownRenderer,
    ) -> None:

        self._prompt_builder = prompt_builder

        self._engine = engine

        self._renderer = renderer

    def generate(
        self,
        context: AssistantContext,
        provider: str,
    ) -> RenderedResponse:

        context.request = (
            self._prompt_builder.build(
                context.job.explanation,
            )
        )

        response = self._engine.generate(
            context,
            provider,
        )

        return self._renderer.render(
            response,
        )