from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.rules.execution.high_cost_node_rule import (
    HighCostNodeRule,
)
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.shared.constants import HIGH_COST_NODE_THRESHOLD


def test_detects_high_cost_node():

    plan = ExecutionPlan(
        node_type="Sort",
        total_cost=HIGH_COST_NODE_THRESHOLD + 1,
    )

    rule = HighCostNodeRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert len(findings) == 1

    finding = next(iter(findings))

    assert finding.code == "HIGH_COST_NODE"
    assert finding.title == "High Cost Operation"


def test_ignores_low_cost_node():

    plan = ExecutionPlan(
        node_type="Sort",
        total_cost=HIGH_COST_NODE_THRESHOLD - 1,
    )

    rule = HighCostNodeRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert findings.is_empty()