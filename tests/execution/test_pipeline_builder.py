import pytest

from backend.execution.demo.end_node import EndNode
from backend.execution.demo.middle_node import MiddleNode
from backend.execution.demo.start_node import StartNode
from backend.execution.contracts.exceptions import PipelineValidationError
from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import (
    NodeDefinition,
    PipelineDefinition,
)
from backend.execution.pipeline.registry import NodeRegistry


def build_registry():

    registry = NodeRegistry()

    registry.register(StartNode())
    registry.register(MiddleNode())
    registry.register(EndNode())

    return registry


def test_build_pipeline():

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

    pipeline = PipelineBuilder(build_registry()).build(definition)

    assert pipeline.definition.pipeline_id == "demo"

    assert len(pipeline.nodes) == 3


def test_unknown_node():

    definition = PipelineDefinition(
        pipeline_id="demo",
        version="1.0",
        entry_node="start",
        nodes=(
            NodeDefinition("start"),
            NodeDefinition("unknown"),
        ),
    )

    with pytest.raises(PipelineValidationError):
        PipelineBuilder(build_registry()).build(definition)