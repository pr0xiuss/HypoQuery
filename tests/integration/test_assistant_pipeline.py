from backend.assistant.assistant_context import (
    AssistantContext,
)
from backend.assistant.assistant_state.job import (
    AssistantJob,
)
from backend.assistant.engine import (
    AssistantEngine,
)
from backend.assistant.models.ai_request import (
    AIRequest,
)
from backend.assistant.models.prompt import (
    Prompt,
)
from backend.assistant.providers.mock_provider import (
    MockProvider,
)
from backend.assistant.registry.provider_registry import (
    ProviderRegistry,
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


def test_assistant_pipeline():

    registry = ProviderRegistry()

    registry.register(
        "mock",
        MockProvider(),
    )

    engine = AssistantEngine(
        registry,
    )

    context = AssistantContext(
        job=AssistantJob(
            explanation=ExplanationSnapshot(
                metadata=ExplanationMetadata(
                    objective="integration",
                    section_count=0,
                ),
                explanation=Explanation(),
            ),
        ),
    )

    context.request = AIRequest(
        prompt=Prompt(
            system="System",
            user="User",
        ),
    )

    response = engine.generate(
        context,
        "mock",
    )

    assert response.content == "Mock response generated."

    assert context.response == response