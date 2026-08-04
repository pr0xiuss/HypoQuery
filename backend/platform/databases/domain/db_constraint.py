from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseConstraint:
    """
    Represents a database constraint.
    """

    id: UUID

    connection_id: UUID

    schema_name: str

    table_name: str

    name: str

    constraint_type: str