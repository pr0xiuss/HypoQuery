from backend.execution.contracts.context import PipelineContext
from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.job import PipelineJob
from backend.execution.contracts.node_result import NodeStatus
from backend.optimization.analysis.composition import (
    build_analysis_engine,
)
from backend.optimization.nodes.plan_analyze_node import (
    PlanAnalyzeNode,
)
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.execution.contracts.enums import JobPriority
from backend.shared.constants import LARGE_TABLE_SCAN_ROWS
from uuid import uuid4

def create_execution() -> PipelineExecution:

    job = PipelineJob(
        source="unit-test",
        pipeline_version="1.0",
        priority=JobPriority.NORMAL,
    )

    context = PipelineContext(
        execution_id=uuid4(),
        trace_id=job.trace_id,
        pipeline_name="optimization",
        pipeline_version="1.0",
        database="test_db",
        schema="public",
    )

    return PipelineExecution(
        job=job,
        context=context,
    )


def test_plan_analyze_node_returns_failure_when_plan_missing():

    node = PlanAnalyzeNode(
        build_analysis_engine(),
    )

    execution = create_execution()

    result = node.execute(
        execution,
    )

    assert result.status == NodeStatus.FAILED


def test_plan_analyze_node_stores_analysis_result():

    node = PlanAnalyzeNode(
        build_analysis_engine(),
    )

    execution = create_execution()

    execution.state.execution_plan = ExecutionPlan(
        node_type="Seq Scan",
        actual_rows=LARGE_TABLE_SCAN_ROWS,
    )

    result = node.execute(
        execution,
    )

    assert result.status == NodeStatus.SUCCESS

    assert execution.state.analysis_result is not None

    assert any(
        finding.code == "LARGE_TABLE_SCAN"
        for finding in execution.state.analysis_result.findings
    )