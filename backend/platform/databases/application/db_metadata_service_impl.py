from uuid import uuid4
from uuid import UUID

from backend.platform.databases.application.db_metadata_service import (
    DatabaseMetadataService,
)
from backend.platform.databases.domain.db_metadata import (
    DatabaseMetadata,
)
from backend.platform.databases.dto.db_discovery_result import (
    DatabaseDiscoveryResult,
)
from backend.platform.databases.repositories.db_metadata_repo import (
    DatabaseMetadataRepository,
)


class DatabaseMetadataServiceImpl(
    DatabaseMetadataService,
):
    def __init__(
        self,
        repository: DatabaseMetadataRepository,
    ):
        self._repository = repository

    def save(
        self,
        connection_id: UUID,
        discovery_result: DatabaseDiscoveryResult,
    ) -> DatabaseMetadata:
        metadata = DatabaseMetadata(
            id=uuid4(),
            connection_id=connection_id,
            postgres_version=discovery_result.postgres_version,
            schemas=discovery_result.schemas,
            tables=discovery_result.tables,
            views=discovery_result.views,
            functions=discovery_result.functions,
            indexes=discovery_result.indexes,
            triggers=discovery_result.triggers,
            sequences=discovery_result.sequences,
            extensions=discovery_result.extensions,
        )

        return self._repository.save(
            metadata,
        )

    def get(
        self,
        connection_id: UUID,
    ) -> DatabaseMetadata | None:
        return self._repository.get_by_connection_id(
            connection_id,
        )

    def refresh(
        self,
        connection_id: UUID,
        discovery_result: DatabaseDiscoveryResult,
    ) -> DatabaseMetadata:
        self._repository.delete_by_connection_id(
            connection_id,
        )

        return self.save(
            connection_id,
            discovery_result,
        )