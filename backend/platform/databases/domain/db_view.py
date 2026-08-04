from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class DatabaseView:
    """
    Represents a database view discovered during onboarding.
    """

    id: UUID

    connection_id: UUID

    schema_name: str

    name: str