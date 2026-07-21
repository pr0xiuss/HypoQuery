from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseIndex:
    """
    Represents a database index discovered during onboarding.
    """

    id: UUID

    connection_id: UUID

    schema_name: str

    table_name: str

    name: str