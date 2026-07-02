from backend.execution.lifecycle.enums import ExecutionStatus


def test_execution_status_values() -> None:
    assert ExecutionStatus.CREATED.value == "created"
    assert ExecutionStatus.QUEUED.value == "queued"
    assert ExecutionStatus.ASSIGNED.value == "assigned"
    assert ExecutionStatus.RUNNING.value == "running"
    assert ExecutionStatus.COMPLETED.value == "completed"
    assert ExecutionStatus.FAILED.value == "failed"
    assert ExecutionStatus.CANCELLED.value == "cancelled"


def test_execution_status_count() -> None:
    assert len(ExecutionStatus) == 7