from abc import ABC
from abc import abstractmethod
from uuid import UUID

from backend.platform.databases.dto.db_overview_response import (
    DatabaseOverviewResponse,
)


class DatabaseOverviewService(ABC):
    @abstractmethod
    def get(
        self,
        connection_id: UUID,
    ) -> DatabaseOverviewResponse:
        pass