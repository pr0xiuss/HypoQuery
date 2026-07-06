from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.validation.comparison.plan_comparator import (
    PlanComparator,
)


def test_compare_detects_improvement():

    comparator = PlanComparator()

    before = ExecutionPlan(
        node_type="Seq Scan",
        total_cost=100.0,
        actual_rows=1000,
    )

    after = ExecutionPlan(
        node_type="Index Scan",
        total_cost=25.0,
        actual_rows=1000,
    )

    metrics = comparator.compare(
        before,
        after,
    )

    assert metrics.cost_reduced is True
    assert metrics.plan_changed is True
    assert metrics.before_cost == 100.0
    assert metrics.after_cost == 25.0