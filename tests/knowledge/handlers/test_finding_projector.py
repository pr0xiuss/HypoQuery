from uuid import uuid4

from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.knowledge.models.enums import KnowledgeNodeType
from backend.knowledge.projection.builders.finding_node_builder import (
    FindingNodeBuilder,
)
from backend.knowledge.projection.context import ProjectionContext
from backend.knowledge.projection.handlers.finding_projector import (
    FindingProjector,
)
from backend.knowledge.projection.job import ProjectionJob
from backend.optimization.analysis.models.finding import Finding
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


def test_finding_projector_projects_nodes():

    finding = Finding(
        category=FindingCategory.EXECUTION,
        code="SEQ_SCAN",
        title="Sequential Scan",
        description="Detected.",
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

    projector = FindingProjector(
        node_builder=FindingNodeBuilder(),
    )

    projector.project(
        context=context,
        graph=context.graph,
    )

    assert context.graph.node_count() == 1

    assert context.graph.nodes_by_type(
        KnowledgeNodeType.FINDING,
    )