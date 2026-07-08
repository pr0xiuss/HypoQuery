from __future__ import annotations

from backend.optimization.recommendation.models.recommendation import (
    Recommendation,
)


class IndexStatementBuilder:
    """
    Builds CREATE INDEX statements from recommendations.
    """

    def build(self, recommendation: Recommendation) -> str:

        relation = (
            recommendation.location.relation
            if recommendation.location is not None
            else None
        )

        columns = (
            recommendation.metadata.attributes.get(
                "filter_columns",
            )
            if recommendation.metadata is not None
            else None
        )

        if relation is None:
            raise ValueError(
                "Recommendation relation is missing."
            )

        if not columns:
            raise ValueError(
                "Recommendation filter columns are missing."
            )

        column_list = ", ".join(
            columns,
        )

        index_name = (
            f"idx_{relation}_{'_'.join(columns)}"
        )

        return (
            f"CREATE INDEX {index_name} "
            f"ON {relation} ({column_list})"
        )