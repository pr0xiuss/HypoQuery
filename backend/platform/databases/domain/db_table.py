from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseTable:
    id: UUID

    connection_id: UUID

    schema_name: str

    name: str

    estimated_rows: int | None

    size_bytes: int

    column_count: int

    has_primary_key: bool