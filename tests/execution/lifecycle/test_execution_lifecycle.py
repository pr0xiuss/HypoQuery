from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.execution.lifecycle.enums import ExecutionStatus
from backend.execution.lifecycle.exceptions import InvalidStateTransitionError
from backend.execution.lifecycle.execution_lifecycle import ExecutionLifecycle


def build_execution() -> PipelineExecution:
    job = PipelineJob(
        source="benchmark",
        pipeline_version="1.0",
    )

    return PipelineExecution(
        job=job,
        context=PipelineContext(
            execution_id=job.job_id,
            trace_id=job.trace_id,
            pipeline_name="optimization_pipeline",
            pipeline_version=job.pipeline_version,
            database="postgres",
            schema="public",
        ),
    )


def test_initial_status_is_created() -> None:
    execution = build_execution()

    assert execution.state.status == ExecutionStatus.CREATED


def test_complete_lifecycle() -> None:
    lifecycle = ExecutionLifecycle()
    execution = build_execution()

    lifecycle.queue(execution)
    assert execution.state.status == ExecutionStatus.QUEUED

    lifecycle.assign(execution)
    assert execution.state.status == ExecutionStatus.ASSIGNED

    lifecycle.start(execution)
    assert execution.state.status == ExecutionStatus.RUNNING

    lifecycle.complete(execution)
    assert execution.state.status == ExecutionStatus.COMPLETED


def test_failed_lifecycle() -> None:
    lifecycle = ExecutionLifecycle()
    execution = build_execution()

    lifecycle.queue(execution)
    lifecycle.assign(execution)
    lifecycle.start(execution)
    lifecycle.fail(execution)

    assert execution.state.status == ExecutionStatus.FAILED


def test_cancel_from_created() -> None:
    lifecycle = ExecutionLifecycle()
    execution = build_execution()

    lifecycle.cancel(execution)

    assert execution.state.status == ExecutionStatus.CANCELLED


def test_invalid_transition_raises_exception() -> None:
    lifecycle = ExecutionLifecycle()
    execution = build_execution()

    try:
        lifecycle.complete(execution)
        assert False
    except InvalidStateTransitionError:
        assert True


def test_completed_state_is_terminal() -> None:
    lifecycle = ExecutionLifecycle()
    execution = build_execution()

    lifecycle.queue(execution)
    lifecycle.assign(execution)
    lifecycle.start(execution)
    lifecycle.complete(execution)

    try:
        lifecycle.start(execution)
        assert False
    except InvalidStateTransitionError:
        assert True


def test_failed_state_is_terminal() -> None:
    lifecycle = ExecutionLifecycle()
    execution = build_execution()

    lifecycle.queue(execution)
    lifecycle.assign(execution)
    lifecycle.start(execution)
    lifecycle.fail(execution)

    try:
        lifecycle.complete(execution)
        assert False
    except InvalidStateTransitionError:
        assert True


def test_cancelled_state_is_terminal() -> None:
    lifecycle = ExecutionLifecycle()
    execution = build_execution()

    lifecycle.cancel(execution)

    try:
        lifecycle.queue(execution)
        assert False
    except InvalidStateTransitionError:
        assert True