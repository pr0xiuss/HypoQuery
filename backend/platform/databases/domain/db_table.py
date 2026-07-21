from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseTable:
    """
    Represents a database table discovered during onboarding.
    """

    id: UUID

    connection_id: UUID

    schema_name: str

    name: str