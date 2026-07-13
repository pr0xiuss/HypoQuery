from backend.operations.cases.context import (
    CaseContext,
)
from backend.operations.cases.repositories.memory_repository import (
    MemoryCaseRepository,
)
from backend.operations.cases.builders.case_builder import (
    CaseBuilder,
)
from backend.operations.cases.engine import (
    CaseEngine,
)
from backend.operations.cases.service import (
    CaseService,
)


def test_context_creates_dependencies() -> None:
    context = CaseContext(
        repository=MemoryCaseRepository(),
    )

    assert isinstance(
        context.repository,
        MemoryCaseRepository,
    )

    assert isinstance(
        context.builder,
        CaseBuilder,
    )

    assert isinstance(
        context.engine,
        CaseEngine,
    )

    assert isinstance(
        context.service,
        CaseService,
    )