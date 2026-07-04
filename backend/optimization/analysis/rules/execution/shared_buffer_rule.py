from __future__ import annotations

from backend.shared.constants import (
    HIGH_SHARED_READ_BLOCKS,
)
from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.categories import FindingCategory
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)
from backend.optimization.analysis.models.location import FindingLocation
from backend.optimization.analysis.models.metadata import FindingMetadata
from backend.optimization.analysis.models.severity import FindingSeverity
from backend.optimization.analysis.rules.base_rule import AnalysisRule
from backend.optimization.analysis.traversal.execution_plan_traverser import (
    ExecutionPlanTraverser,
)


class SharedBufferRule(AnalysisRule):
    """
    Detects execution plan nodes that perform excessive shared
    block reads from disk.
    """

    def __init__(
        self,
        traverser: ExecutionPlanTraverser,
    ) -> None:
        self._traverser = traverser

    @property
    def name(self) -> str:
        return "shared_buffer"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        findings = FindingCollection()

        for node in self._traverser.depth_first(context.execution_plan):

            if node.shared_read_blocks <= HIGH_SHARED_READ_BLOCKS:
                continue

            findings.add(
                Finding(
                    category=FindingCategory.EXECUTION,
                    code="HIGH_SHARED_READS",
                    title="High Shared Buffer Reads",
                    description=(
                        f"Execution node performed "
                        f"{node.shared_read_blocks} shared block reads."
                    ),
                    severity=FindingSeverity.MEDIUM,
                    location=FindingLocation(
                        relation=node.relation_name,
                        schema=node.schema_name,
                    ),
                    metadata=FindingMetadata(
                        attributes={
                            "shared_read_blocks": node.shared_read_blocks,
                            "shared_hit_blocks": node.shared_hit_blocks,
                            "estimated_rows": node.estimated_rows,
                            "actual_rows": node.actual_rows,
                            "total_cost": node.total_cost,
                        }
                    ),
                )
            )

        return findings