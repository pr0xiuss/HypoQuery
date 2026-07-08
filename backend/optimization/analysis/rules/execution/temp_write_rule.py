from __future__ import annotations

from backend.shared.constants import (
    TEMP_WRITTEN_BLOCKS_THRESHOLD,
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


class TempWriteRule(AnalysisRule):
    """
    Detects execution plan nodes that spill temporary data to disk.
    """

    def __init__(
        self,
        traverser: ExecutionPlanTraverser,
    ) -> None:
        self._traverser = traverser

    @property
    def name(self) -> str:
        return "temp_write"

    def analyze(
        self,
        context: AnalysisContext,
    ) -> FindingCollection:

        findings = FindingCollection()

        for node in self._traverser.depth_first(context.execution_plan):

            if node.temp_written_blocks <= TEMP_WRITTEN_BLOCKS_THRESHOLD:
                continue

            findings.add(
                Finding(
                    category=FindingCategory.EXECUTION,
                    code="TEMP_DISK_WRITES",
                    title="Temporary Disk Writes",
                    description=(
                        f"Execution node wrote "
                        f"{node.temp_written_blocks} temporary blocks to disk."
                    ),
                    severity=FindingSeverity.MEDIUM,
                    location=FindingLocation(
                        relation=node.relation_name,
                        schema=node.schema_name,
                    ),
                    metadata=FindingMetadata(
                        attributes={
                            "temp_written_blocks": node.temp_written_blocks,
                            "temp_read_blocks": node.temp_read_blocks,
                            "estimated_rows": node.estimated_rows,
                            "actual_rows": node.actual_rows,
                            "total_cost": node.total_cost,
                        }
                    ),
                )
            )

        return findings