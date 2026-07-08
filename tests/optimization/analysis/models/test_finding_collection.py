from backend.optimization.analysis.models.categories import FindingCategory
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.analysis.models.location import FindingLocation
from backend.optimization.analysis.models.metadata import FindingMetadata
from backend.optimization.analysis.models.severity import FindingSeverity


def test_creates_finding():

    finding = Finding(
        category=FindingCategory.EXECUTION,
        code="LARGE_TABLE_SCAN",
        title="Large Sequential Scan",
        description="Sequential scan processed many rows.",
        severity=FindingSeverity.HIGH,
        location=FindingLocation(
            relation="users",
            schema="public",
        ),
        metadata=FindingMetadata(
            attributes={
                "rows": 500000,
            }
        ),
    )

    assert finding.category == FindingCategory.EXECUTION
    assert finding.code == "LARGE_TABLE_SCAN"
    assert finding.title == "Large Sequential Scan"
    assert finding.description == "Sequential scan processed many rows."
    assert finding.severity == FindingSeverity.HIGH

    assert finding.location.relation == "users"
    assert finding.location.schema == "public"

    assert finding.metadata.attributes["rows"] == 500000

    assert finding.id is not None
    assert finding.observed_at is not None