from backend.optimization.analysis.models.analysis_result import (
    AnalysisResult,
)
from backend.optimization.analysis.models.categories import FindingCategory
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.analysis.models.severity import FindingSeverity


def test_total_findings():

    result = AnalysisResult()

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="ONE",
            title="One",
            description="One",
            severity=FindingSeverity.HIGH,
        )
    )

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="TWO",
            title="Two",
            description="Two",
            severity=FindingSeverity.HIGH,
        )
    )

    assert result.total_findings == 2