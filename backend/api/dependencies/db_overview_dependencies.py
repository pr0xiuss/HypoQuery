from backend.platform.databases.application.db_overview_service import (
    DatabaseOverviewService,
)
from backend.platform.databases.application.db_overview_service_impl import (
    DatabaseOverviewServiceImpl,
)
from backend.api.dependencies.db_connection_dependencies import get_database_metadata_repository


def get_database_overview_service() -> DatabaseOverviewService:
    return DatabaseOverviewServiceImpl(
        repository=get_database_metadata_repository(),
    )