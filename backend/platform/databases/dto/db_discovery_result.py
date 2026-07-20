from pydantic import BaseModel
from pydantic import ConfigDict

from backend.platform.databases.dto.db_statistics_result import (
    DatabaseStatisticsResult,
)


class DatabaseDiscoveryResult(BaseModel):
    """
    Result of database discovery.
    """

    postgres_version: str

    schemas: list[str]

    tables: list[str]

    views: list[str]

    functions: list[str]

    indexes: list[str]

    triggers: list[str]

    sequences: list[str]

    extensions: list[str]

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