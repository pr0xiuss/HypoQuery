from backend.optimization.rules.base_rule import (
    BaseRule,
)
from backend.optimization.models.optimization_finding import (
    OptimizationFinding,
)


class TempWriteRule(BaseRule):

    def check(self, plan):

        if plan.temp_written_blocks == 0:
            return []

        return [
            OptimizationFinding(
                issue="Temporary Disk Writes",
                severity="MEDIUM",
                recommendation="Increase work_mem or optimize sorting.",
                node_type=plan.node_type,
                estimated_cost=plan.total_cost,
                estimated_rows=plan.estimated_rows,
            )
        ]
