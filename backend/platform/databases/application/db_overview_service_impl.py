from uuid import UUID

from backend.platform.databases.application.db_overview_service import (
    DatabaseOverviewService,
)
from backend.platform.databases.dto.db_overview_response import (
    DatabaseOverviewResponse,
)
from backend.platform.databases.repositories.db_metadata_repo import (
    DatabaseMetadataRepository,
)


class DatabaseOverviewServiceImpl(
    DatabaseOverviewService,
):
    def __init__(
        self,
        repository: DatabaseMetadataRepository,
    ):
        self._repository = repository

    def get(
        self,
        connection_id: UUID,
    ) -> DatabaseOverviewResponse:
        metadata = self._repository.get_by_connection_id(
            connection_id,
        )

        if metadata is None:
            raise ValueError(
                "Database metadata not found.",
            )

        return DatabaseOverviewResponse(
            postgres_version=metadata.postgres_version,
            database_size=metadata.database_size,
            schemas=len(metadata.schemas),
            tables=len(metadata.tables),
            views=len(metadata.views),
            functions=len(metadata.functions),
            indexes=len(metadata.indexes),
            triggers=len(metadata.triggers),
            sequences=len(metadata.sequences),
            extensions=len(metadata.extensions),
            database_statistics=metadata.database_statistics,
            connection_statistics=metadata.connection_statistics,
            lock_statistics=metadata.lock_statistics,
            last_refreshed=metadata.last_refreshed.isoformat(),
        )