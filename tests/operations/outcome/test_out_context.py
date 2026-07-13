from backend.operations.outcome.builders.outcome_builder import (
    OutcomeBuilder,
)
from backend.operations.outcome.context import (
    OutcomeContext,
)
from backend.operations.outcome.engine import (
    OutcomeEngine,
)
from backend.operations.outcome.repositories.memory_repository import (
    MemoryOutcomeRepository,
)
from backend.operations.outcome.service import (
    OutcomeService,
)


def test_context_creates_dependencies() -> None:
    context = OutcomeContext(
        repository=MemoryOutcomeRepository(),
    )

    assert isinstance(
        context.repository,
        MemoryOutcomeRepository,
    )

    assert isinstance(
        context.builder,
        OutcomeBuilder,
    )

    assert isinstance(
        context.engine,
        OutcomeEngine,
    )

    assert isinstance(
        context.service,
        OutcomeService,
    )