from dataclasses import dataclass

from infrastructure.postgres.scripts.models.enums import (
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
    sql: str