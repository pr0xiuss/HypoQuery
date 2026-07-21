from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseMetadata:
    """
    Represents the discovered metadata for a database connection.
    """

    id: UUID

    connection_id: UUID

    postgres_version: str

    schemas: list[str]

    tables: list[str]

    views: list[str]

    functions: list[str]

    indexes: list[str]

    triggers: list[str]

    sequences: list[str]

    extensions: list[str]