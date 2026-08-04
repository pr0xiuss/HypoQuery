from uuid import UUID

from backend.platform.databases.application.db_metadata_service import DatabaseMetadataService
from backend.platform.databases.domain.db_metadata import DatabaseMetadata
from backend.platform.databases.dto.db_discovery_result import DatabaseDiscoveryResult
from backend.platform.databases.application.db_metadata_mapper import DatabaseMetadataMapper
from backend.platform.databases.repositories.db_metadata_repo import DatabaseMetadataRepository


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
        metadata = DatabaseMetadataMapper.to_domain(
            connection_id=connection_id,
            discovery_result=discovery_result,
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