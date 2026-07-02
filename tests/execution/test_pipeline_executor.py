from uuid import uuid4

from backend.execution.bus.in_process_event_bus import InProcessEventBus
from backend.execution.bus.subscriber_registry import SubscriberRegistry
from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.enums import PipelineStatus
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.execution.events.execution_event_factory import (
    ExecutionEventFactory,
)
from backend.execution.events.execution_event_metadata_provider import (
    ExecutionEventMetadataProvider,
)
from backend.execution.lifecycle.execution_lifecycle import (
    ExecutionLifecycle,
)
from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import (
    NodeDefinition,
    PipelineDefinition,
)
from backend.execution.pipeline.executor import PipelineExecutor
from backend.execution.pipeline.registry import NodeRegistry
from backend.execution.publisher.event_publisher import EventPublisher
from backend.execution.runtime.execution_runtime import ExecutionRuntime
from backend.execution.runtime.node_runtime import NodeRuntime
from backend.execution.runtime.runtime_context import RuntimeContext
from backend.execution.runtime.system_clock import SystemClock

from backend.execution.demo.end_node import EndNode
from backend.execution.demo.middle_node import MiddleNode
from backend.execution.demo.start_node import StartNode


def build_executor() -> PipelineExecutor:
    lifecycle = ExecutionLifecycle()

    metadata_provider = ExecutionEventMetadataProvider()

    event_factory = ExecutionEventFactory(
        metadata_provider,
    )

    subscriber_registry = SubscriberRegistry()

    event_bus = InProcessEventBus(
        subscriber_registry,
    )

    publisher = EventPublisher(
        event_bus,
    )

    runtime_context = RuntimeContext(
        lifecycle=lifecycle,
        event_factory=event_factory,
        publisher=publisher,
        clock=SystemClock(),
    )

    runtime = ExecutionRuntime(
        runtime_context,
    )

    node_runtime = NodeRuntime(
        runtime_context,
    )

    return PipelineExecutor(
        runtime=runtime,
        node_runtime=node_runtime,
    )


def build_execution() -> PipelineExecution:
    execution_id = uuid4()
    trace_id = uuid4()

    return PipelineExecution(
        job=PipelineJob(
            source="demo",
            pipeline_version="1.0",
            job_id=execution_id,
            trace_id=trace_id,
        ),
        context=PipelineContext(
            execution_id=execution_id,
            trace_id=trace_id,
            pipeline_name="demo",
            pipeline_version="1.0",
            database="demo",
            schema="public",
        ),
    )


def test_pipeline_execution() -> None:
    registry = NodeRegistry()

    registry.register(StartNode())
    registry.register(MiddleNode())
    registry.register(EndNode())

    definition = PipelineDefinition(
        pipeline_id="demo",
        version="1.0",
        entry_node="start",
        nodes=(
            NodeDefinition("start"),
            NodeDefinition("middle"),
            NodeDefinition("end"),
        ),
        edges={
            "start": ("middle",),
            "middle": ("end",),
            "end": (),
        },
    )

    pipeline = PipelineBuilder(
        registry,
    ).build(definition)

    execution = build_execution()

    result = build_executor().execute(
        pipeline,
        execution,
    )

    assert result.status == PipelineStatus.COMPLETED

    assert execution.state.artifacts["started"] is True

    assert execution.state.artifacts["finished"] is True

    assert execution.state.artifacts["counter"] == 1

    assert len(execution.state.errors) == 0