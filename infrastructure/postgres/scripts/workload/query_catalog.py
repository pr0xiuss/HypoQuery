from pathlib import Path

from infrastructure.postgres.scripts.models.query import Query
from infrastructure.postgres.scripts.workload.metadata_parser import (
    MetadataParser,
)


class QueryCatalog:

    QUERY_DIRECTORY = (
        Path(__file__).parent / "queries"
    )

    @classmethod
    def get_queries(cls) -> list[Query]:

        queries = []

        sql_files = sorted(
            cls.QUERY_DIRECTORY.rglob("*.sql")
        )

        for sql_file in sql_files:

            content = sql_file.read_text(
                encoding="utf-8"
            )

            lines = content.splitlines()

            metadata = MetadataParser.parse(lines)

            sql = "\n".join(
                line
                for line in lines
                if not line.startswith("--")
            ).strip()

            queries.append(
                Query(
                    id=metadata["id"],
                    name=metadata["name"],
                    category=metadata["category"],
                    difficulty=metadata["difficulty"],
                    expected_issue=metadata["expected_issue"],
                    sql=sql,
                )
            )

        return queries