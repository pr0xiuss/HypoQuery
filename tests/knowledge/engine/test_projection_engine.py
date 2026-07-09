from uuid import uuid4

from backend.knowledge.projection.builders.finding_node_builder import (
    FindingNodeBuilder,
)
from backend.knowledge.projection.builders.finding_relationship_builder import (
    FindingRelationshipBuilder,
)
from backend.knowledge.projection.context import (
    ProjectionContext,
)
from backend.knowledge.projection.engine import (
    ProjectionEngine,
)
from backend.knowledge.projection.handlers.finding_projector import (
    FindingProjector,
)
from backend.knowledge.projection.job import (
    ProjectionJob,
)
from backend.knowledge.projection.registry.projection_registry import (
    ProjectionRegistry,
)
from backend.optimization.history.models.execution_metadata import (
    ExecutionMetadata,
)
from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)
from backend.optimization.history.models.execution_summary import (
    ExecutionSummary,
)
from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from tests.knowledge.fixtures import (
    build_finding,
)


def test_projection_engine_projects_graph() -> None:

    snapshot = OptimizationSnapshot(
        summary=ReportSummary(),
        findings=(
            build_finding(),
        ),
    )

    execution = ExecutionRecord(
        metadata=ExecutionMetadata(
            execution_id=uuid4(),
            trace_id=uuid4(),
            fingerprint="test",
            normalized_sql="SELECT 1",
            pipeline_name="knowledge",
            pipeline_version="1.0",
            database="hypoquery",
            schema="public",
        ),
        summary=ExecutionSummary(),
        snapshot=snapshot,
    )

    context = ProjectionContext(
        job=ProjectionJob(
            execution=execution,
        ),
    )

    registry = ProjectionRegistry()

    registry.register(
        FindingProjector(
            node_builder=FindingNodeBuilder(),
            relationship_builder=FindingRelationshipBuilder(),
        )
    )

    engine = ProjectionEngine(
        registry=registry,
    )

    graph = engine.project(
        context=context,
    )

    assert len(graph.nodes) == 1