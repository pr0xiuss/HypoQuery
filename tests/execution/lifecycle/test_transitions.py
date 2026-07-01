from backend.execution.lifecycle.enums import ExecutionStatus
from backend.execution.lifecycle.transitions import VALID_TRANSITIONS


def test_created_transitions() -> None:
    assert VALID_TRANSITIONS[ExecutionStatus.CREATED] == {
        ExecutionStatus.QUEUED,
        ExecutionStatus.CANCELLED,
    }


def test_queued_transitions() -> None:
    assert VALID_TRANSITIONS[ExecutionStatus.QUEUED] == {
        ExecutionStatus.ASSIGNED,
        ExecutionStatus.CANCELLED,
    }


def test_assigned_transitions() -> None:
    assert VALID_TRANSITIONS[ExecutionStatus.ASSIGNED] == {
        ExecutionStatus.RUNNING,
        ExecutionStatus.FAILED,
        ExecutionStatus.CANCELLED,
    }


def test_running_transitions() -> None:
    assert VALID_TRANSITIONS[ExecutionStatus.RUNNING] == {
        ExecutionStatus.COMPLETED,
        ExecutionStatus.FAILED,
        ExecutionStatus.CANCELLED,
    }


def test_completed_is_terminal() -> None:
    assert VALID_TRANSITIONS[ExecutionStatus.COMPLETED] == set()


def test_failed_is_terminal() -> None:
    assert VALID_TRANSITIONS[ExecutionStatus.FAILED] == set()


def test_cancelled_is_terminal() -> None:
    assert VALID_TRANSITIONS[ExecutionStatus.CANCELLED] == set()