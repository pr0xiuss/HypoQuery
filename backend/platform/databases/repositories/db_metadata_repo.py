from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.databases.domain.db_metadata import (
    DatabaseMetadata,
)


class DatabaseMetadataRepository(ABC):
    """
    Repository for database metadata.
    """

    @abstractmethod
    def save(
        self,
        metadata: DatabaseMetadata,
    ) -> DatabaseMetadata:
        raise NotImplementedError

    @abstractmethod
    def get_by_connection_id(
        self,
        connection_id: UUID,
    ) -> DatabaseMetadata | None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_connection_id(
        self,
        connection_id: UUID,
    ) -> None:
        raise NotImplementedError