from uuid import uuid4

from backend.knowledge.models.enums import (
    KnowledgeNodeType,
)
from backend.knowledge.models.knowledge_node import (
    KnowledgeNode,
)
from backend.knowledge.models.node_key import (
    NodeKey,
)
from backend.knowledge.projection.builders.graph_snapshot_builder import (
    GraphSnapshotBuilder,
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
from backend.knowledge.projection.engine import (
    ProjectionEngine,
)
from backend.knowledge.projection.handlers.recommendation_projector import (
    RecommendationProjector,
)
from backend.knowledge.projection.job import (
    ProjectionJob,
)
from backend.knowledge.projection.registry.projection_registry import (
    ProjectionRegistry,
)
from backend.knowledge.projection.service import (
    KnowledgeProjectionService,
)
from backend.knowledge.repositories.memory_repository import (
    MemoryKnowledgeRepository,
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
from backend.optimization.recommendation.models.metadata import (
    RecommendationMetadata,
)
from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)
from backend.optimization.recommendation.models.category import (
    RecommendationCategory,
)
from backend.optimization.recommendation.models.recommendation_key import (
    RecommendationKey,
)
from backend.optimization.recommendation.models.priority import (
    RecommendationPriority,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


def test_projection_pipeline():

    recommendation = Recommendation(
        category=RecommendationCategory.INDEX,
        code="CREATE_INDEX",
        key=RecommendationKey(
            category="index",
            target="users",
            action="create",
        ),
        title="Create Index",
        description="Create Index",
        priority=RecommendationPriority.HIGH,
        metadata=RecommendationMetadata(
            originating_findings=["SEQ_SCAN"],
        ),
    )

    snapshot = OptimizationSnapshot(
        summary=ReportSummary(),
        recommendations=(recommendation,),
    )

    execution = ExecutionRecord(
        metadata=ExecutionMetadata(
            execution_id=uuid4(),
            trace_id=uuid4(),
            fingerprint="fp",
            normalized_sql="SELECT 1",
            pipeline_name="knowledge",
            pipeline_version="1.0",
            database="postgres",
            schema="public",
        ),
        summary=ExecutionSummary(),
        snapshot=snapshot,
    )

    registry = ProjectionRegistry()

    registry.register(
        RecommendationProjector(
            node_builder=RecommendationNodeBuilder(),
            relationship_builder=RecommendationRelationshipBuilder(),
        )
    )

    service = KnowledgeProjectionService(
        engine=ProjectionEngine(
            registry,
        ),
        snapshot_builder=GraphSnapshotBuilder(),
        repository=MemoryKnowledgeRepository(),
    )

    context = ProjectionContext(
        job=ProjectionJob(
            execution=execution,
        ),
    )

    context.graph.add_node(
        KnowledgeNode(
            key=NodeKey("finding:SEQ_SCAN"),
            type=KnowledgeNodeType.FINDING,
        )
    )

    graph_snapshot = service.project(
        context,
    )

    assert len(graph_snapshot.nodes) == 1
    assert len(graph_snapshot.relationships) == 0