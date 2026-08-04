from datetime import datetime, UTC
from uuid import UUID, uuid4
from backend.platform.databases.domain.db_metadata import DatabaseMetadata
from backend.platform.databases.dto.db_discovery_result import DatabaseDiscoveryResult


class DatabaseMetadataMapper:
    """
    Maps discovery results into domain metadata objects.
    """

    @staticmethod
    def to_domain(
        connection_id: UUID,
        discovery_result: DatabaseDiscoveryResult,
    ) -> DatabaseMetadata:
        return DatabaseMetadata(
            id=uuid4(),
            connection_id=connection_id,
            postgres_version=discovery_result.postgres_version,
            database_size=discovery_result.database_size,
            settings=discovery_result.settings,
            replication=discovery_result.replication,
            database_statistics=discovery_result.database_statistics,
            table_statistics=discovery_result.table_statistics,
            index_statistics=discovery_result.index_statistics,
            connection_statistics=discovery_result.connection_statistics,
            lock_statistics=discovery_result.lock_statistics,
            schemas=discovery_result.schemas,
            tables=discovery_result.tables,
            columns=discovery_result.columns,
            constraints=discovery_result.constraints,
            views=discovery_result.views,
            functions=discovery_result.functions,
            indexes=discovery_result.indexes,
            triggers=discovery_result.triggers,
            sequences=discovery_result.sequences,
            extensions=discovery_result.extensions,
            last_refreshed=datetime.now(UTC),
        )