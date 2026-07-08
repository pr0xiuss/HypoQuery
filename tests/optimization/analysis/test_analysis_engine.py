from backend.optimization.analysis.composition import (
    build_analysis_engine,
)
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.shared.constants import LARGE_TABLE_SCAN_ROWS


def test_analysis_engine_returns_analysis_result():

    engine = build_analysis_engine()

    plan = ExecutionPlan(
        node_type="Seq Scan",
        actual_rows=LARGE_TABLE_SCAN_ROWS,
    )

    result = engine.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert result is not None

    assert result.total_findings > 0

    assert any(
        finding.code == "LARGE_TABLE_SCAN"
        for finding in result.findings
    )