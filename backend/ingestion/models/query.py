from dataclasses import dataclass

from backend.models.enums import (
    Difficulty,
    ExpectedIssue,
    QueryCategory,
)


@dataclass(slots=True)
class Query:

    id: str

    name: str

    category: QueryCategory

    difficulty: Difficulty

    expected_issue: ExpectedIssue

    description: str

    expected_fix: str

    sql: str
