from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseExtension:
    """
    Represents a PostgreSQL extension discovered during onboarding.
    """

    id: UUID

    connection_id: UUID

    name: str

    version: str