from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseSequence:
    """
    Represents a database sequence discovered during onboarding.
    """

    id: UUID

    connection_id: UUID

    schema_name: str

    name: str