from infrastructure.postgres.scripts.common.db import (
    get_connection,
)
from infrastructure.postgres.scripts.observability.collectors.explain_collector import (
    ExplainCollector,
)
from infrastructure.postgres.scripts.observability.parsers.explain_parser import (
    ExplainParser,
)


def test_explain_pipeline():

    connection = get_connection()

    collector = ExplainCollector(connection)

    parser = ExplainParser()

    explain = collector.collect(
        "SELECT * FROM products;"
    )

    plan = parser.parse(explain)

    assert plan.node_type == "Seq Scan"

    connection.close()