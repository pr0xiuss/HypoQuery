from uuid import uuid4

from backend.knowledge.projection.builders.finding_node_builder import (
    FindingNodeBuilder,
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
from backend.optimization.analysis.models.finding import (
    Finding,
)
from backend.optimization.analysis.models.categories import (
    FindingCategory,
)
from backend.optimization.analysis.models.severity import (
    FindingSeverity,
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


def build_execution():

    finding = Finding(
        category=FindingCategory.EXECUTION,
        code="SEQ_SCAN",
        title="Sequential Scan",
        description="Detected",
        severity=FindingSeverity.HIGH,
    )

    return ExecutionRecord(
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
        snapshot=OptimizationSnapshot(
            summary=ReportSummary(),
            findings=(finding,),
        ),
    )


def test_projection_is_deterministic():

    registry = ProjectionRegistry()

    registry.register(
        FindingProjector(
            node_builder=FindingNodeBuilder(),
        )
    )

    service = KnowledgeProjectionService(
        engine=ProjectionEngine(
            registry,
        ),
        snapshot_builder=GraphSnapshotBuilder(),
        repository=MemoryKnowledgeRepository(),
    )

    first = service.project(
        ProjectionContext(
            job=ProjectionJob(
                execution=build_execution(),
            ),
        )
    )

    second = service.project(
        ProjectionContext(
            job=ProjectionJob(
                execution=build_execution(),
            ),
        )
    )

    assert tuple(
        node.key
        for node in first.nodes
    ) == tuple(
        node.key
        for node in second.nodes
    )

    assert tuple(
        relationship.key
        for relationship in first.relationships
    ) == tuple(
        relationship.key
        for relationship in second.relationships
    )