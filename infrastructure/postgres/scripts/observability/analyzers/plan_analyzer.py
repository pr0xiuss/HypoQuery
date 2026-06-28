from infrastructure.postgres.scripts.observability.analyzers.rules.shared_buffer_rule import (
    SharedBufferRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.seq_scan_rule import (
    SeqScanRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.temp_write_rule import (
    TempWriteRule,
)
from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)
from infrastructure.postgres.scripts.observability.models.optimization_finding import (
    OptimizationFinding,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.hash_join_rule import (
    HashJoinRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.nested_loop_rule import (
    NestedLoopRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.hash_aggregate_rule import (
    HashAggregateRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.sort_rule import (
    SortRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.bitmap_scan_rule import (
    BitmapScanRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.merge_join_rule import (
    MergeJoinRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.index_only_scan_rule import (
    IndexOnlyScanRule,
)
from infrastructure.postgres.scripts.observability.analyzers.rules.index_scan_rule import (
    IndexScanRule,
)


class PlanAnalyzer:

    def __init__(self):

        self.rules = [
            SeqScanRule(),
            SharedBufferRule(),
            TempWriteRule(),
            HashJoinRule(),
            NestedLoopRule(),
            HashAggregateRule(),
            SortRule(),
            MergeJoinRule(),
            BitmapScanRule(),
            IndexScanRule(),
            IndexOnlyScanRule(),
        ]

    def analyze(
        self,
        plan: ExecutionPlan,
    ) -> list[OptimizationFinding]:

        findings = []

        self._traverse(
            plan,
            findings,
        )

        return self._aggregate(findings)

    def _traverse(
        self,
        plan: ExecutionPlan,
        findings: list[OptimizationFinding],
    ) -> None:

        for rule in self.rules:
            findings.extend(rule.check(plan))

        for child in plan.children:
            self._traverse(
                child,
                findings,
            )

    def _aggregate(
        self,
        findings: list[OptimizationFinding],
    ) -> list[OptimizationFinding]:

        grouped = {}

        for finding in findings:
            if finding.issue not in grouped:
                grouped[finding.issue] = {
                    "finding": finding,
                    "count": 1,
                }
            else:
                grouped[finding.issue]["count"] += 1

        aggregated = []

        for item in grouped.values():
            finding = item["finding"]
            count = item["count"]

            if count > 1:
                finding = OptimizationFinding(
                    issue=f"{finding.issue} ({count} occurrences)",
                    severity=finding.severity,
                    recommendation=finding.recommendation,
                    node_type=finding.node_type,
                    estimated_cost=finding.estimated_cost,
                    estimated_rows=finding.estimated_rows,
                )

            aggregated.append(finding)

        return aggregated
