from uuid import UUID

from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.execution.events.execution_event_metadata_provider import (
    ExecutionEventMetadataProvider,
)
from backend.execution.events.version import CURRENT_EVENT_VERSION


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


def test_create_metadata() -> None:
    provider = ExecutionEventMetadataProvider()

    execution = build_execution()

    metadata = provider.create(execution)

    assert isinstance(metadata.event_id, UUID)
    assert isinstance(metadata.execution_id, UUID)
    assert isinstance(metadata.trace_id, UUID)

    assert metadata.execution_id == execution.context.execution_id
    assert metadata.trace_id == execution.context.trace_id

    assert metadata.sequence_number == 1
    assert metadata.event_version == CURRENT_EVENT_VERSION


def test_sequence_number_increments() -> None:
    provider = ExecutionEventMetadataProvider()

    execution = build_execution()

    first = provider.create(execution)
    second = provider.create(execution)
    third = provider.create(execution)

    assert first.sequence_number == 1
    assert second.sequence_number == 2
    assert third.sequence_number == 3


def test_reset_sequence() -> None:
    provider = ExecutionEventMetadataProvider()

    execution = build_execution()

    provider.create(execution)
    provider.create(execution)

    provider.reset(execution.context.execution_id)

    metadata = provider.create(execution)

    assert metadata.sequence_number == 1