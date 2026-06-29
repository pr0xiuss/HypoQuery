from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.fingerprint import QueryFingerprint
from backend.execution.contracts.job import PipelineJob
from backend.execution.contracts.enums import PipelineStatus

from backend.execution.demo.end_node import EndNode
from backend.execution.demo.middle_node import MiddleNode
from backend.execution.demo.start_node import StartNode

from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import (
    NodeDefinition,
    PipelineDefinition,
)
from backend.execution.pipeline.executor import PipelineExecutor
from backend.execution.pipeline.registry import NodeRegistry


def test_pipeline_execution():

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

    pipeline = PipelineBuilder(registry).build(definition)

    execution = PipelineExecution(
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

    result = PipelineExecutor().execute(
        pipeline,
        execution,
    )

    assert result.status == PipelineStatus.COMPLETED

    assert execution.state.artifacts["started"] is True

    assert execution.state.artifacts["finished"] is True

    assert execution.state.artifacts["counter"] == 1

    assert len(execution.state.errors) == 0