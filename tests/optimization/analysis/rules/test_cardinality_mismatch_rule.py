from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.rules.execution.cardinality_mismatch_rule import (
    CardinalityMismatchRule,
)
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.optimization.models.execution_plan import ExecutionPlan


def test_detects_cardinality_mismatch():

    plan = ExecutionPlan(
        node_type="Seq Scan",
        estimated_rows=100,
        actual_rows=10000,
    )

    rule = CardinalityMismatchRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert len(findings) == 1

    finding = next(iter(findings))

    assert finding.code == "CARDINALITY_MISMATCH"
    assert finding.title == "Cardinality Mismatch"


def test_ignores_accurate_estimates():

    plan = ExecutionPlan(
        node_type="Seq Scan",
        estimated_rows=1000,
        actual_rows=1050,
    )

    rule = CardinalityMismatchRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert findings.is_empty()