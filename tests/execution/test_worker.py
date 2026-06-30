from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.fingerprint import QueryFingerprint
from backend.execution.contracts.job import PipelineJob
from backend.execution.contracts.enums import PipelineStatus

from backend.execution.demo.start_node import StartNode
from backend.execution.demo.middle_node import MiddleNode
from backend.execution.demo.end_node import EndNode

from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import (
    NodeDefinition,
    PipelineDefinition,
)
from backend.execution.pipeline.executor import PipelineExecutor
from backend.execution.pipeline.registry import NodeRegistry

from backend.execution.queue.job_record import QueueEntry
from backend.execution.queue.memory_queue import InMemoryQueue

from backend.execution.workers.worker import Worker


def build_pipeline():

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

    return PipelineBuilder(registry).build(definition)


def build_execution():

    return PipelineExecution(
        job=PipelineJob(
            source="demo",
            pipeline_version="1.0",
        ),
        context=PipelineContext(
            fingerprint=QueryFingerprint(
                normalized_sql="SELECT 1",
                hash="demo",
            ),
            database="demo",
            schema="public",
        ),
    )


def test_worker_process():

    queue = InMemoryQueue()

    queue.enqueue(
        QueueEntry(
            execution=build_execution()
        )
    )

    worker = Worker(
        queue,
        PipelineExecutor(),
    )

    result = worker.process(
        build_pipeline()
    )

    assert result is not None
    assert result.status == PipelineStatus.COMPLETED


def test_worker_empty_queue():

    worker = Worker(
        InMemoryQueue(),
        PipelineExecutor(),
    )

    assert worker.process(
        build_pipeline()
    ) is None