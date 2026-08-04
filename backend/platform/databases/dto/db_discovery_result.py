from pydantic import BaseModel
from pydantic import ConfigDict
from backend.platform.databases.dto.db_statistics_result import DatabaseStatisticsResult
from backend.platform.databases.domain.db_extension import DatabaseExtension
from backend.platform.databases.domain.db_function import DatabaseFunction
from backend.platform.databases.domain.db_index import DatabaseIndex
from backend.platform.databases.domain.db_schema import DatabaseSchema
from backend.platform.databases.domain.db_sequence import DatabaseSequence
from backend.platform.databases.domain.db_table import DatabaseTable
from backend.platform.databases.domain.db_trigger import DatabaseTrigger
from backend.platform.databases.domain.db_view import DatabaseView
from backend.platform.databases.domain.db_column import DatabaseColumn
from backend.platform.databases.domain.db_constraint import DatabaseConstraint


class DatabaseDiscoveryResult(BaseModel):
    """
    Result of database discovery.
    """

    postgres_version: str

    schemas: list[DatabaseSchema]

    tables: list[DatabaseTable]

    columns: list[DatabaseColumn]

    constraints: list[DatabaseConstraint]

    views: list[DatabaseView]

    functions: list[DatabaseFunction]

    indexes: list[DatabaseIndex]

    triggers: list[DatabaseTrigger]

    sequences: list[DatabaseSequence]

    extensions: list[DatabaseExtension]

    database_size: int

    settings: dict[str, str]

    replication: dict[str, int | bool]

    database_statistics: DatabaseStatisticsResult

    table_statistics: list[dict[str, int | str]]

    index_statistics: list[dict[str, int | str]]

    connection_statistics: dict[str, int]

    lock_statistics: dict[str, int]

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )