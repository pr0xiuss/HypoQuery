from backend.optimization.rules.shared_buffer_rule import (
    SharedBufferRule,
)
from backend.optimization.rules.seq_scan_rule import (
    SeqScanRule,
)
from backend.optimization.rules.temp_write_rule import (
    TempWriteRule,
)
from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)
from backend.optimization.models.optimization_finding import (
    OptimizationFinding,
)
from backend.optimization.rules.hash_join_rule import (
    HashJoinRule,
)
from backend.optimization.rules.nested_loop_rule import (
    NestedLoopRule,
)
from backend.optimization.rules.hash_aggregate_rule import (
    HashAggregateRule,
)
from backend.optimization.rules.sort_rule import (
    SortRule,
)
from backend.optimization.rules.bitmap_scan_rule import (
    BitmapScanRule,
)
from backend.optimization.rules.merge_join_rule import (
    MergeJoinRule,
)
from backend.optimization.rules.index_only_scan_rule import (
    IndexOnlyScanRule,
)
from backend.optimization.rules.index_scan_rule import (
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
