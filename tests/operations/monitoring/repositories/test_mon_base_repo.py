from backend.operations.monitoring.repositories.base_repository import (
    BaseMonitoringRepository,
)


def test_base_repository_is_abstract() -> None:
    assert BaseMonitoringRepository.__abstractmethods__ == {
        "add",
        "find",
        "contains",
    }