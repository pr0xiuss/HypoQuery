from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseIndex:
    id: UUID

    connection_id: UUID

    schema_name: str

    table_name: str

    name: str

    method: str

    unique: bool

    primary: bool