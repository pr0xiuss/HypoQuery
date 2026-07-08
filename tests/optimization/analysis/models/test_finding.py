from backend.optimization.analysis.models.categories import FindingCategory
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.analysis.models.finding_collection import (
    FindingCollection,
)
from backend.optimization.analysis.models.severity import FindingSeverity


def create_finding(code: str) -> Finding:

    return Finding(
        category=FindingCategory.EXECUTION,
        code=code,
        title=code,
        description=code,
        severity=FindingSeverity.HIGH,
    )


def test_add_finding():

    collection = FindingCollection()

    collection.add(
        create_finding("ONE")
    )

    assert len(collection) == 1
    assert not collection.is_empty()


def test_extend_collection():

    first = FindingCollection()
    second = FindingCollection()

    first.add(
        create_finding("ONE")
    )

    second.add(
        create_finding("TWO")
    )

    first.extend(second)

    assert len(first) == 2

    codes = [
        finding.code
        for finding in first
    ]

    assert codes == [
        "ONE",
        "TWO",
    ]