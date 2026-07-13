from backend.operations.cases.repositories.base_repository import (
    BaseCaseRepository,
)


def test_base_repository_is_abstract() -> None:
    assert BaseCaseRepository.__abstractmethods__ == {
        "add",
        "find",
        "contains",
    }