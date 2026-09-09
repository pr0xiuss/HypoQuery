import pytest

from backend.models.enums import (
    Difficulty,
    ExpectedIssue,
    QueryCategory,
)
from backend.ingestion.metadata_parser import (
    MetadataParser,
)


def test_parse_valid_metadata():

    lines = [
        "-- id: TEST001",
        "-- name: Test Query",
        "-- category: SEQUENTIAL_SCAN",
        "-- difficulty: EASY",
        "-- expected_issue: SEQUENTIAL_SCAN",
        "-- description: Test description",
        "-- expected_fix: Create an index",
        "",
        "SELECT * FROM products;",
    ]

    metadata = MetadataParser.parse(lines)

    assert metadata["id"] == "TEST001"
    assert metadata["name"] == "Test Query"
    assert metadata["category"] == QueryCategory.SEQUENTIAL_SCAN
    assert metadata["difficulty"] == Difficulty.EASY
    assert (
        metadata["expected_issue"]
        == ExpectedIssue.SEQUENTIAL_SCAN
    )
    assert metadata["description"] == "Test description"
    assert metadata["expected_fix"] == "Create an index"


def test_missing_required_field():

    lines = [
        "-- name: Missing ID",
    ]

    with pytest.raises(KeyError):
        MetadataParser.parse(lines)


def test_stops_parsing_after_sql():

    lines = [
        "-- id: TEST001",
        "-- name: Test",
        "-- category: SEQUENTIAL_SCAN",
        "-- difficulty: EASY",
        "-- expected_issue: SEQUENTIAL_SCAN",
        "-- description: desc",
        "-- expected_fix: fix",
        "",
        "SELECT * FROM products;",
        "-- id: SHOULD_NOT_PARSE",
    ]

    metadata = MetadataParser.parse(lines)

    assert metadata["id"] == "TEST001"