from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.rules.execution.sort_rule import (
    SortRule,
)
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)
from backend.optimization.models.execution_plan import ExecutionPlan
from backend.shared.constants import LARGE_SORT_COST


def test_detects_expensive_sort():

    plan = ExecutionPlan(
        node_type="Sort",
        total_cost=LARGE_SORT_COST,
    )

    rule = SortRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert len(findings) == 1

    finding = next(iter(findings))

    assert finding.code == "EXPENSIVE_SORT"
    assert finding.title == "Expensive Sort"


def test_ignores_small_sort():

    plan = ExecutionPlan(
        node_type="Sort",
        total_cost=LARGE_SORT_COST - 1,
    )

    rule = SortRule(
        ExecutionPlanTraverser(),
    )

    findings = rule.analyze(
        AnalysisContext(
            execution_plan=plan,
        )
    )

    assert findings.is_empty()