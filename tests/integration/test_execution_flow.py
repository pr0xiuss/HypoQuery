from backend.execution.demo.start_node import StartNode
from backend.execution.demo.middle_node import MiddleNode
from backend.execution.demo.end_node import EndNode

from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import (
    PipelineDefinition,
    NodeDefinition,
)
from backend.execution.pipeline.registry import (
    NodeRegistry,
)

from tests.execution.test_pipeline_executor import (
    build_execution,
    build_executor,
)


def build_pipeline():

    registry = NodeRegistry()

    registry.register(StartNode())
    registry.register(MiddleNode())
    registry.register(EndNode())

    definition = PipelineDefinition(
        pipeline_id="integration",
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

    return PipelineBuilder(
        registry,
    ).build(
        definition,
    )


def test_execution_flow():
    pipeline = build_pipeline()

    execution = build_execution()

    executor = build_executor()

    result = executor.execute(
        pipeline,
        execution,
    )

    assert result.status.value == "completed"

    assert execution.state.artifacts["started"]

    assert execution.state.artifacts["finished"]

    assert execution.state.artifacts["counter"] == 1

    assert len(execution.state.errors) == 0