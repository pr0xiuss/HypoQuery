from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseSchema:
    """
    Represents a database schema discovered during onboarding.
    """

    id: UUID

    connection_id: UUID

    name: str