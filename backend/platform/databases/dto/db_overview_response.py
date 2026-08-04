from pydantic import BaseModel

from backend.platform.databases.dto.db_statistics_result import (
    DatabaseStatisticsResult,
)


class DatabaseOverviewResponse(BaseModel):
    postgres_version: str
    database_size: int

    schemas: int
    tables: int
    views: int
    functions: int
    indexes: int
    triggers: int
    sequences: int
    extensions: int

    database_statistics: DatabaseStatisticsResult

    connection_statistics: dict
    lock_statistics: dict

    last_refreshed: str