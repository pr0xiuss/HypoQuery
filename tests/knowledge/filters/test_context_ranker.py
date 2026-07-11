from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)
from backend.knowledge.models.optimization_context import (
    OptimizationContext,
)
from backend.knowledge.ranking.context_ranker import (
    ContextRanker,
)


def test_context_ranker():

    context = OptimizationContext()

    context.add_section(
        ContextSection(
            title="Strategy",
            priority=ContextPriority.SUPPORTING,
        )
    )

    context.add_section(
        ContextSection(
            title="Recommendation",
            priority=ContextPriority.PRIMARY,
        )
    )

    ContextRanker().rank(
        context,
    )

    assert (
        context.sections[0].priority
        == ContextPriority.PRIMARY
    )

    assert (
        context.sections[1].priority
        == ContextPriority.SUPPORTING
    )