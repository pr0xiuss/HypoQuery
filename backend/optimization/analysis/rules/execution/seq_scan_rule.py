from __future__ import annotations

from backend.optimization.analysis.context import AnalysisContext
from backend.optimization.analysis.models.categories import FindingCategory
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.analysis.models.finding_collection import FindingCollection
from backend.optimization.analysis.models.location import FindingLocation
from backend.optimization.analysis.models.metadata import FindingMetadata
from backend.optimization.analysis.models.severity import FindingSeverity
from backend.optimization.analysis.rules.base_rule import AnalysisRule
from backend.optimization.analysis.traversal.execution_plan_traverser import ExecutionPlanTraverser
from backend.optimization.analysis.parsers.predicate_parser import PredicateParser
from backend.shared.constants import LARGE_TABLE_SCAN_ROWS


class SeqScanRule(AnalysisRule):
    """
    Detects large sequential scans.

    Small sequential scans are normal and intentionally ignored.
    """

    def __init__(self, traverser: ExecutionPlanTraverser, predicate_parser: PredicateParser,) -> None:

        self._traverser = traverser
        self._predicate_parser = predicate_parser


    @property
    def name(self) -> str:
        return "large_table_scan"

    def analyze(self, context: AnalysisContext,) -> FindingCollection:

        findings = FindingCollection()

        for node in self._traverser.depth_first(context.execution_plan):

            if node.node_type != "Seq Scan":
                continue

            if node.actual_rows < LARGE_TABLE_SCAN_ROWS:
                continue

            filter_columns = (self._predicate_parser.extract_columns(node.filter_condition))

            findings.add(
                Finding(
                    category=FindingCategory.EXECUTION,
                    code="LARGE_TABLE_SCAN",
                    title="Large Sequential Scan",
                    description=(
                        f"Sequential scan processed "
                        f"{node.actual_rows:,} rows."
                    ),
                    severity=FindingSeverity.HIGH,
                    location=FindingLocation(
                        relation=node.relation_name,
                        schema=node.schema_name,
                    ),
                    metadata=FindingMetadata(
                        attributes={
                            "actual_rows": node.actual_rows,
                            "estimated_rows": node.estimated_rows,
                            "startup_cost": node.startup_cost,
                            "total_cost": node.total_cost,
                            "shared_read_blocks": node.shared_read_blocks,
                            "filter_condition": node.filter_condition,
                            "filter_columns": filter_columns,
                        }
                    ),
                )
            )

        return findings