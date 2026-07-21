from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.databases.dto.db_health_result import (
    DatabaseHealthResult,
)


class DatabaseConnectionMonitorService(ABC):
    """
    Provides operational monitoring for database connections.
    """

    @abstractmethod
    def health(
        self,
        connection_id: UUID,
    ) -> DatabaseHealthResult:
        raise NotImplementedError