from uuid import UUID
from dataclasses import dataclass

@dataclass(slots=True, kw_only=True)
class DatabaseColumn:
    id: UUID

    connection_id: UUID

    schema_name: str

    table_name: str

    name: str

    data_type: str

    nullable: bool

    default_value: str | None

    ordinal_position: int