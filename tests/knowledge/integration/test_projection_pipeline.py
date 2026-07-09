from uuid import uuid4

from backend.knowledge.projection.builders.finding_node_builder import (
    FindingNodeBuilder,
)
from backend.knowledge.projection.builders.finding_relationship_builder import (
    FindingRelationshipBuilder,
)
from backend.knowledge.projection.builders.graph_snapshot_builder import (
    GraphSnapshotBuilder,
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
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)
from tests.knowledge.fixtures import (
    build_finding,
)


def test_projection_pipeline_end_to_end() -> None:

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
            fingerprint="pipeline",
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

    service = KnowledgeProjectionService(
        engine=ProjectionEngine(
            registry=registry,
        ),
        snapshot_builder=GraphSnapshotBuilder(),
        repository=MemoryKnowledgeRepository(),
    )

    graph_snapshot = service.project(
        context=context,
    )

    assert len(graph_snapshot.nodes) == 1
    assert len(graph_snapshot.relationships) == 0