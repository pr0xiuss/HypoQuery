from infrastructure.postgres.scripts.observability.analyzers.rules.base_rule import (
    BaseRule,
)
from infrastructure.postgres.scripts.observability.models.optimization_finding import (
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
                recommendation=("Increase work_mem or optimize sorting."),
            )
        ]
