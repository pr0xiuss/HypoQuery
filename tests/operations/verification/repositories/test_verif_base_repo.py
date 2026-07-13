from backend.operations.verification.repositories.base_repository import (
    BaseVerificationRepository,
)


def test_base_repository_is_abstract() -> None:
    assert BaseVerificationRepository.__abstractmethods__ == {
        "add",
        "find",
        "contains",
    }