from backend.operations.policy.builders.policy_builder import (
    PolicyBuilder,
)
from backend.operations.policy.context import (
    PolicyContext,
)
from backend.operations.policy.engine import (
    PolicyEngine,
)
from backend.operations.policy.repositories.memory_repository import (
    MemoryPolicyRepository,
)
from backend.operations.policy.service import (
    PolicyService,
)


def test_context_creates_dependencies() -> None:
    context = PolicyContext(
        repository=MemoryPolicyRepository(),
    )

    assert isinstance(
        context.repository,
        MemoryPolicyRepository,
    )

    assert isinstance(
        context.builder,
        PolicyBuilder,
    )

    assert isinstance(
        context.engine,
        PolicyEngine,
    )

    assert isinstance(
        context.service,
        PolicyService,
    )