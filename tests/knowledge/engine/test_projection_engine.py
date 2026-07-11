from uuid import uuid4

from backend.knowledge.projection.builders.finding_node_builder import (
    FindingNodeBuilder,
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


def test_projection_engine():

    finding = Finding(
        category=FindingCategory.EXECUTION,
        code="SEQ_SCAN",
        title="Sequential Scan",
        description="Detected",
        severity=FindingSeverity.HIGH,
    )

    snapshot = OptimizationSnapshot(
        summary=ReportSummary(),
        findings=(finding,),
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

    context = ProjectionContext(
        job=ProjectionJob(
            execution=execution,
        ),
    )

    registry = ProjectionRegistry()

    registry.register(
        FindingProjector(
            node_builder=FindingNodeBuilder(),
        )
    )

    engine = ProjectionEngine(
        registry,
    )

    graph = engine.project(
        context,
    )

    assert graph.node_count() == 1

    assert graph.relationship_count() == 0