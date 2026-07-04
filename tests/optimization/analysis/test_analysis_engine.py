from backend.optimization.analysis.composition import (
    build_analysis_engine,
)
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.models.execution_plan import ExecutionPlan


def test_analysis_engine_detects_large_seq_scan():

    plan = ExecutionPlan(
        node_type="Seq Scan",
        relation_name="users",
        estimated_rows=500000,
        actual_rows=500000,
        total_cost=25000,
    )

    engine = build_analysis_engine()

    context = AnalysisContext(
        execution_plan=plan,
    )

    result = engine.analyze(context)

    assert result is not None
    assert result.total_findings > 0

    findings = list(result.findings)

    assert any(
        finding.code == "LARGE_TABLE_SCAN"
        and finding.title == "Large Sequential Scan"
        for finding in findings
    )