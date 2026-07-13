from backend.operations.verification.builders.verification_builder import (
    VerificationBuilder,
)
from backend.operations.verification.context import (
    VerificationContext,
)
from backend.operations.verification.engine import (
    VerificationEngine,
)
from backend.operations.verification.repositories.memory_repository import (
    MemoryVerificationRepository,
)
from backend.operations.verification.service import (
    VerificationService,
)


def test_context_creates_dependencies() -> None:
    context = VerificationContext(
        repository=MemoryVerificationRepository(),
    )

    assert isinstance(
        context.repository,
        MemoryVerificationRepository,
    )

    assert isinstance(
        context.builder,
        VerificationBuilder,
    )

    assert isinstance(
        context.engine,
        VerificationEngine,
    )

    assert isinstance(
        context.service,
        VerificationService,
    )