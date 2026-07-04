from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.rules.execution.hash_aggregate_rule import (
    HashAggregateRule,
)
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.shared.constants import LARGE_HASH_AGGREGATE_ROWS


def test_detects_large_hash_aggregate():

    plan = ExecutionPlan(
        node_type="HashAggregate",
        actual_rows=LARGE_HASH_AGGREGATE_ROWS,
    )

    rule = HashAggregateRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert len(findings) == 1

    finding = next(iter(findings))

    assert finding.code == "LARGE_HASH_AGGREGATE"
    assert finding.title == "Large Hash Aggregate"


def test_ignores_small_hash_aggregate():

    plan = ExecutionPlan(
        node_type="HashAggregate",
        actual_rows=LARGE_HASH_AGGREGATE_ROWS - 1,
    )

    rule = HashAggregateRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert findings.is_empty()