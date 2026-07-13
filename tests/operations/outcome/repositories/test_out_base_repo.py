from backend.operations.outcome.repositories.base_repository import (
    BaseOutcomeRepository,
)


def test_base_repository_is_abstract() -> None:
    assert BaseOutcomeRepository.__abstractmethods__ == {
        "add",
        "find",
        "contains",
    }