from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.projection.builders.validation_node_builder import (
    ValidationNodeBuilder,
)
from backend.knowledge.projection.builders.validation_relationship_builder import (
    ValidationRelationshipBuilder,
)
from backend.knowledge.projection.context import (
    ProjectionContext,
)
from backend.knowledge.projection.handlers.validation_projector import (
    ValidationProjector,
)
from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from tests.knowledge.fixtures import (
    build_validation,
)
from uuid import uuid4

from backend.knowledge.projection.job import ProjectionJob
from backend.optimization.history.models.execution_metadata import (
    ExecutionMetadata,
)
from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)
from backend.optimization.history.models.execution_summary import (
    ExecutionSummary,
)

def test_validation_projector_projects_nodes() -> None:

    snapshot = OptimizationSnapshot(
        summary=ReportSummary(),
        validations=(
            build_validation(),
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

    job = ProjectionJob(
        execution=execution,
    )

    context = ProjectionContext(
        job=job,
    )

    graph = KnowledgeGraph()

    projector = ValidationProjector(
        node_builder=ValidationNodeBuilder(),
        relationship_builder=ValidationRelationshipBuilder(),
    )

    projector.project(
        context=context,
        graph=graph,
    )

    assert len(graph.nodes) == 1
    assert len(graph.relationships) == 0