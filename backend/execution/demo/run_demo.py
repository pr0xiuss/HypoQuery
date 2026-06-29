from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.fingerprint import QueryFingerprint
from backend.execution.contracts.job import PipelineJob

from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import (
    NodeDefinition,
    PipelineDefinition,
)
from backend.execution.pipeline.executor import PipelineExecutor
from backend.execution.pipeline.registry import NodeRegistry

from backend.execution.demo.start_node import StartNode
from backend.execution.demo.middle_node import MiddleNode
from backend.execution.demo.end_node import EndNode


def main():

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

    fingerprint = QueryFingerprint(
        normalized_sql="SELECT 1",
        hash="demo_hash",
    )

    context = PipelineContext(
        fingerprint=fingerprint,
        database="demo_db",
        schema="public",
    )

    job = PipelineJob(
        source="demo",
        pipeline_version="1.0",
    )

    execution = PipelineExecution(
        job=job,
        context=context,
    )

    executor = PipelineExecutor()

    result = executor.execute(
        pipeline,
        execution,
    )

    print("=" * 50)
    print("Pipeline Status :", result.status.value)
    print("Artifacts       :", execution.state.artifacts)
    print("Metrics         :", execution.state.metrics)
    print("Errors          :", execution.state.errors)
    print("Duration (ms)   :", result.duration_ms)
    print("=" * 50)


if __name__ == "__main__":
    main()