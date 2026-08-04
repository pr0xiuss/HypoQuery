from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.databases.domain.db_metadata import (
    DatabaseMetadata,
)
from backend.platform.databases.dto.db_discovery_result import (
    DatabaseDiscoveryResult,
)


class DatabaseMetadataService(ABC):
    """
    Manages persisted database metadata.
    """

    @abstractmethod
    def save(
        self,
        connection_id: UUID,
        discovery_result: DatabaseDiscoveryResult,
    ) -> DatabaseMetadata:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        connection_id: UUID,
    ) -> DatabaseMetadata | None:
        raise NotImplementedError

    @abstractmethod
    def refresh(
        self,
        connection_id: UUID,
        discovery_result: DatabaseDiscoveryResult,
    ) -> DatabaseMetadata:
        raise NotImplementedError