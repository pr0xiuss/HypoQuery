from __future__ import annotations

from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.validation.models.improvement_metrics import (
    ImprovementMetrics,
)


class PlanComparator:
    """
    Compares two execution plans and produces improvement metrics.
    """

    def compare(self, original: ExecutionPlan, candidate: ExecutionPlan,) -> ImprovementMetrics:

        before = original.total_cost

        after = candidate.total_cost

        delta = after - before

        if before > 0:
            improvement = (
                (before - after) / before
            ) * 100.0
        else:
            improvement = 0.0

        return ImprovementMetrics(
            before_cost=before,
            after_cost=after,
            cost_delta=delta,
            improvement_percent=improvement,
            before_rows=original.actual_rows,
            after_rows=candidate.actual_rows,
            plan_changed=(
                original.node_type
                != candidate.node_type
            ),
            cost_reduced=after < before,
        )