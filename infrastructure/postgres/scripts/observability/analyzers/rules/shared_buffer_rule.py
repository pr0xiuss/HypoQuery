from infrastructure.postgres.scripts.observability.analyzers.rules.base_rule import (
    BaseRule,
)
from infrastructure.postgres.scripts.observability.models.optimization_finding import (
    OptimizationFinding,
)
from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)

class SharedBufferRule(BaseRule):

    def check(self, plan: ExecutionPlan) -> list[OptimizationFinding]:

        if plan.shared_read_blocks <= 100:
            return []

        return [
            OptimizationFinding(
                issue="High Disk Reads",
                severity="MEDIUM",
                recommendation=(
                    "High shared disk reads detected. "
                    "Consider adding indexes, increasing cache "
                    "efficiency, or reviewing frequently accessed queries."
                ),
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]