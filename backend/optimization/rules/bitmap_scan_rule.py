from backend.optimization.rules.base_rule import (
    BaseRule,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.models.optimization_finding import (
    OptimizationFinding,
)


class BitmapScanRule(BaseRule):

    def check(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        if plan.node_type not in (
            "Bitmap Heap Scan",
            "Bitmap Index Scan",
        ):
            return []

        return [
            OptimizationFinding(
                issue="Bitmap Scan Detected",
                severity="LOW",
                recommendation=(
                    "Bitmap scans are efficient for medium "
                    "selectivity queries. Verify that "
                    "appropriate indexes exist."
                ),
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]
