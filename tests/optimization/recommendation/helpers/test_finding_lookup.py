from backend.optimization.analysis.models.analysis_result import (
    AnalysisResult,
)
from backend.optimization.analysis.models.categories import (
    FindingCategory,
)
from backend.optimization.analysis.models.finding import (
    Finding,
)
from backend.optimization.analysis.models.severity import (
    FindingSeverity,
)
from backend.optimization.recommendation.context import (
    RecommendationContext,
)
from backend.optimization.recommendation.helpers.finding_lookup import (
    FindingLookup,
)


def create_context() -> RecommendationContext:

    result = AnalysisResult()

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="LARGE_TABLE_SCAN",
            title="Large Sequential Scan",
            description="Large sequential scan detected.",
            severity=FindingSeverity.HIGH,
        )
    )

    result.findings.add(
        Finding(
            category=FindingCategory.EXECUTION,
            code="HIGH_COST_NODE",
            title="High Cost Operation",
            description="High cost operation detected.",
            severity=FindingSeverity.HIGH,
        )
    )

    return RecommendationContext(
        analysis_result=result,
    )


def test_has():

    lookup = FindingLookup(
        create_context(),
    )

    assert lookup.has(
        "LARGE_TABLE_SCAN",
    )

    assert not lookup.has(
        "UNKNOWN",
    )


def test_has_any():

    lookup = FindingLookup(
        create_context(),
    )

    assert lookup.has_any(
        "UNKNOWN",
        "HIGH_COST_NODE",
    )


def test_has_all():

    lookup = FindingLookup(
        create_context(),
    )

    assert lookup.has_all(
        "LARGE_TABLE_SCAN",
        "HIGH_COST_NODE",
    )


def test_get():

    lookup = FindingLookup(
        create_context(),
    )

    finding = lookup.get(
        "LARGE_TABLE_SCAN",
    )

    assert finding is not None

    assert finding.code == "LARGE_TABLE_SCAN"


def test_find_all():

    lookup = FindingLookup(
        create_context(),
    )

    findings = lookup.find_all(
        "LARGE_TABLE_SCAN",
    )

    assert len(findings) == 1


def test_count():

    lookup = FindingLookup(
        create_context(),
    )

    assert lookup.count(
        "LARGE_TABLE_SCAN",
    ) == 1