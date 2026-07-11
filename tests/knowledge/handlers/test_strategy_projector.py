from backend.knowledge.models.knowledge_graph import (
    KnowledgeGraph,
)
from backend.knowledge.projection.builders.strategy_node_builder import (
    StrategyNodeBuilder,
)
from backend.knowledge.projection.builders.strategy_relationship_builder import (
    StrategyRelationshipBuilder,
)
from backend.knowledge.projection.context import (
    ProjectionContext,
)
from backend.knowledge.projection.handlers.strategy_projector import (
    StrategyProjector,
)
from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from tests.knowledge.fixtures import (
    build_strategy,
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

def test_strategy_projector_projects_nodes() -> None:

    snapshot = OptimizationSnapshot(
        summary=ReportSummary(),
        strategies=(
            build_strategy(),
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

    projector = StrategyProjector(
        node_builder=StrategyNodeBuilder(),
        relationship_builder=StrategyRelationshipBuilder(),
    )

    projector.project(
        context=context,
        graph=graph,
    )

    assert len(graph.nodes) == 1
    assert len(graph.relationships) == 0