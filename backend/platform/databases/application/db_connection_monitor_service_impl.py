from uuid import UUID

from backend.platform.databases.application.db_connection_monitor_service import (
    DatabaseConnectionMonitorService,
)
from backend.platform.databases.application.db_health_service import (
    DatabaseHealthService,
)
from backend.platform.databases.dto.db_health_result import (
    DatabaseHealthResult,
)


class DatabaseConnectionMonitorServiceImpl(
    DatabaseConnectionMonitorService,
):
    def __init__(
        self,
        health_service: DatabaseHealthService,
    ):
        self._health_service = health_service

    def health(
        self,
        connection_id: UUID,
    ) -> DatabaseHealthResult:
        return self._health_service.check_health(
            connection_id,
        )