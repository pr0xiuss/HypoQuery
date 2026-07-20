from abc import ABC
from abc import abstractmethod
from uuid import UUID
from backend.platform.databases.dto.db_discovery_result import DatabaseDiscoveryResult


class DatabaseDiscoveryService(ABC):
    """
    Discovers metadata from a registered database.
    """

    @abstractmethod
    def discover(
        self,
        connection_id: UUID,
    ) -> DatabaseDiscoveryResult:
        """
        Performs database discovery.
        """