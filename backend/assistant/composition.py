from __future__ import annotations

from backend.assistant.engine import (
    AssistantEngine,
)
from backend.assistant.prompts.optimization_prompt_builder import (
    OptimizationPromptBuilder,
)
from backend.assistant.providers.gemini_provider import (
    GeminiProvider,
)
from backend.assistant.providers.mock_provider import (
    MockProvider,
)
from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
)
from backend.assistant.renderers.markdown_renderer import (
    MarkdownRenderer,
)
from backend.assistant.service import (
    AssistantService,
)


def build_assistant_service() -> AssistantService:
    """
    Builds the complete assistant pipeline.
    """

    registry = ProviderRegistry()

    registry.register(
        "gemini",
        GeminiProvider(),
    )

    registry.register(
        "mock",
        MockProvider(),
    )

    engine = AssistantEngine(
        registry,
    )

    return AssistantService(
        prompt_builder=OptimizationPromptBuilder(),
        engine=engine,
        renderer=MarkdownRenderer(),
    )