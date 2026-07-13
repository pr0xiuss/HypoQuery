from backend.operations.policy.repositories.base_repository import (
    BasePolicyRepository,
)


def test_base_repository_is_abstract() -> None:
    assert BasePolicyRepository.__abstractmethods__ == {
        "add",
        "find",
        "contains",
    }