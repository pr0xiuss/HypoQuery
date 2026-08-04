from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseFunction:
    """
    Represents a database function discovered during onboarding.
    """

    id: UUID

    connection_id: UUID

    schema_name: str

    name: str

    return_type: str | None