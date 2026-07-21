from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.databases.dto.db_health_result import (
    DatabaseHealthResult,
)


class DatabaseHealthService(ABC):
    """
    Performs health checks against configured database connections.
    """

    @abstractmethod
    def check_health(
        self,
        connection_id: UUID,
    ) -> DatabaseHealthResult:
        raise NotImplementedError