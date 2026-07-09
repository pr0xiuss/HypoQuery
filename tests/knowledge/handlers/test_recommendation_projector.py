from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.projection.builders.recommendation_node_builder import (
    RecommendationNodeBuilder,
)
from backend.knowledge.projection.builders.recommendation_relationship_builder import (
    RecommendationRelationshipBuilder,
)
from backend.knowledge.projection.context import (
    ProjectionContext,
)
from backend.knowledge.projection.handlers.recommendation_projector import (
    RecommendationProjector,
)
from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from tests.knowledge.fixtures import (
    build_recommendation,
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

def test_recommendation_projector_projects_nodes() -> None:

    snapshot = OptimizationSnapshot(
        summary=ReportSummary(),
        recommendations=(
            build_recommendation(),
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

    projector = RecommendationProjector(
        node_builder=RecommendationNodeBuilder(),
        relationship_builder=RecommendationRelationshipBuilder(),
    )

    projector.project(
        context=context,
        graph=graph,
    )

    assert len(graph.nodes) == 1
    assert len(graph.relationships) == 0