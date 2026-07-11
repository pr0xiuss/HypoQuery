from backend.assistant.assistant_context import (
    AssistantContext,
)
from backend.assistant.assistant_state.job import (
    AssistantJob,
)
from backend.assistant.engine import (
    AssistantEngine,
)
from backend.assistant.prompts.optimization_prompt_builder import (
    OptimizationPromptBuilder,
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
from backend.knowledge.models.explanation import (
    Explanation,
)
from backend.knowledge.models.explanation_metadata import (
    ExplanationMetadata,
)
from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)
from backend.knowledge.models.explanation_summary import (
    ExplanationSummary,
)


def test_full_pipeline():

    explanation = Explanation()

    explanation.summary = ExplanationSummary(
        title="Optimization Report",
        overview="Integration test.",
    )

    snapshot = ExplanationSnapshot(
        metadata=ExplanationMetadata(
            objective="integration",
            section_count=0,
        ),
        explanation=explanation,
    )

    registry = ProviderRegistry()

    registry.register(
        "mock",
        MockProvider(),
    )

    service = AssistantService(
        prompt_builder=OptimizationPromptBuilder(),
        engine=AssistantEngine(
            registry,
        ),
        renderer=MarkdownRenderer(),
    )

    rendered = service.generate(
        AssistantContext(
            job=AssistantJob(
                explanation=snapshot,
            ),
        ),
        "mock",
    )

    assert rendered.content == "Mock response generated."

    assert rendered.format == "markdown"