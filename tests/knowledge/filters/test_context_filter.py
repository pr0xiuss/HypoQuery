from backend.knowledge.filters.context_filter import (
    ContextFilter,
)
from backend.knowledge.models.context_priority import (
    ContextPriority,
)
from backend.knowledge.models.context_section import (
    ContextSection,
)


def test_context_filter():

    primary = ContextSection(
        title="Recommendation",
        priority=ContextPriority.PRIMARY,
    )

    secondary = ContextSection(
        title="Validation",
        priority=ContextPriority.SECONDARY,
    )

    filtered = ContextFilter().by_priority(
        (
            primary,
            secondary,
        ),
        ContextPriority.PRIMARY,
    )

    assert len(
        filtered,
    ) == 1

    assert (
        filtered[0].priority
        == ContextPriority.PRIMARY
    )