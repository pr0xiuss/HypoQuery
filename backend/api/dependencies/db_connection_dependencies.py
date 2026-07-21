from fastapi import Depends
from sqlalchemy.orm import Session

from backend.platform.shared.database import get_db_session

from backend.platform.databases.application.db_connection_service import DatabaseConnectionService
from backend.platform.databases.application.db_connection_service_impl import DatabaseConnectionServiceImpl
from backend.platform.databases.application.db_connection_validator import DatabaseConnectionValidator
from backend.platform.databases.application.db_discovery_service import DatabaseDiscoveryService
from backend.platform.databases.application.db_health_service import DatabaseHealthService
from backend.platform.databases.application.db_health_service_impl import DatabaseHealthServiceImpl
from backend.platform.databases.application.db_metadata_persistence_service import DatabaseMetadataPersistenceService
from backend.platform.databases.application.db_metadata_persistence_service_impl import DatabaseMetadataPersistenceServiceImpl
from backend.platform.databases.application.postgres_connection_validator import PostgresConnectionValidator
from backend.platform.databases.application.postgres_connection_statistics_discoverer import PostgresConnectionStatisticsDiscoverer
from backend.platform.databases.application.postgres_db_discovery_service import PostgresDatabaseDiscoveryService
from backend.platform.databases.application.postgres_db_settings_discoverer import PostgresDatabaseSettingsDiscoverer
from backend.platform.databases.application.postgres_db_size_discoverer import PostgresDatabaseSizeDiscoverer
from backend.platform.databases.application.postgres_db_statistics_discoverer import PostgresDatabaseStatisticsDiscoverer
from backend.platform.databases.application.postgres_extension_discoverer import PostgresExtensionDiscoverer
from backend.platform.databases.application.postgres_function_discoverer import PostgresFunctionDiscoverer
from backend.platform.databases.application.postgres_index_discoverer import PostgresIndexDiscoverer
from backend.platform.databases.application.postgres_index_statistics_discoverer import PostgresIndexStatisticsDiscoverer
from backend.platform.databases.application.postgres_lock_statistics_discoverer import PostgresLockStatisticsDiscoverer
from backend.platform.databases.application.postgres_replication_discoverer import PostgresReplicationDiscoverer
from backend.platform.databases.application.postgres_schema_discoverer import PostgresSchemaDiscoverer
from backend.platform.databases.application.postgres_sequence_discoverer import PostgresSequenceDiscoverer
from backend.platform.databases.application.postgres_table_discoverer import PostgresTableDiscoverer
from backend.platform.databases.application.postgres_table_statistics_discoverer import PostgresTableStatisticsDiscoverer
from backend.platform.databases.application.postgres_trigger__discoverer import PostgresTriggerDiscoverer
from backend.platform.databases.application.postgres_version_discoverer import PostgresVersionDiscoverer
from backend.platform.databases.application.postgres_view_discoverer import PostgresViewDiscoverer

from backend.platform.databases.infra.db_connection_repo_impl import DatabaseConnectionRepositoryImpl
from backend.platform.databases.repositories.db_connection_repo import DatabaseConnectionRepository
from backend.platform.databases.repositories.db_metadata_repo import DatabaseMetadataRepository
from backend.platform.databases.repositories.db_metadata_repo_impl import DatabaseMetadataRepositoryImpl


def get_database_metadata_repository(
    session: Session = Depends(
        get_db_session,
    ),
) -> DatabaseMetadataRepository:
    return DatabaseMetadataRepositoryImpl(
        session,
    )

def get_database_health_service(
    session: Session = Depends(
        get_db_session,
    ),
) -> DatabaseHealthService:
    repository = DatabaseConnectionRepositoryImpl(
        session,
    )

    return DatabaseHealthServiceImpl(
        repository,
    )

def get_database_connection_service(
    session: Session = Depends(
        get_db_session,
    ),
) -> DatabaseConnectionService:
    repository = DatabaseConnectionRepositoryImpl(
        session,
    )

    metadata_repository = DatabaseMetadataRepositoryImpl(
        session,
    )

    validator = PostgresConnectionValidator()

    discovery_service = PostgresDatabaseDiscoveryService(
        repository=repository,
        version_discoverer=PostgresVersionDiscoverer(),
        schema_discoverer=PostgresSchemaDiscoverer(),
        extension_discoverer=PostgresExtensionDiscoverer(),
        table_discoverer=PostgresTableDiscoverer(),
        view_discoverer=PostgresViewDiscoverer(),
        function_discoverer=PostgresFunctionDiscoverer(),
        index_discoverer=PostgresIndexDiscoverer(),
        trigger_discoverer=PostgresTriggerDiscoverer(),
        sequence_discoverer=PostgresSequenceDiscoverer(),
        database_settings_discoverer=PostgresDatabaseSettingsDiscoverer(),
        database_size_discoverer=PostgresDatabaseSizeDiscoverer(),
        database_statistics_discoverer=PostgresDatabaseStatisticsDiscoverer(),
        replication_discoverer=PostgresReplicationDiscoverer(),
        table_statistics_discoverer=PostgresTableStatisticsDiscoverer(),
        index_statistics_discoverer=PostgresIndexStatisticsDiscoverer(),
        connection_statistics_discoverer=PostgresConnectionStatisticsDiscoverer(),
        lock_statistics_discoverer=PostgresLockStatisticsDiscoverer(),
    )

    metadata_persistence_service = (
        DatabaseMetadataPersistenceServiceImpl(
            metadata_repository,
        )
    )

    health_service = DatabaseHealthServiceImpl(
        repository,
    )

    return DatabaseConnectionServiceImpl(
        repository=repository,
        validator=validator,
        discovery_service=discovery_service,
        metadata_persistence_service=metadata_persistence_service,
        health_service=health_service,
    )

def get_database_connection_validator() -> DatabaseConnectionValidator:
    return PostgresConnectionValidator()

def get_database_discovery_service(
    session: Session = Depends(
        get_db_session,
    ),
) -> DatabaseDiscoveryService:
    repository = DatabaseConnectionRepositoryImpl(
        session,
    )

    return PostgresDatabaseDiscoveryService(
        repository=repository,
        version_discoverer=PostgresVersionDiscoverer(),
        schema_discoverer=PostgresSchemaDiscoverer(),
        extension_discoverer=PostgresExtensionDiscoverer(),
        table_discoverer=PostgresTableDiscoverer(),
        view_discoverer=PostgresViewDiscoverer(),
        function_discoverer=PostgresFunctionDiscoverer(),
        index_discoverer=PostgresIndexDiscoverer(),
        trigger_discoverer=PostgresTriggerDiscoverer(),
        sequence_discoverer=PostgresSequenceDiscoverer(),
        database_settings_discoverer=PostgresDatabaseSettingsDiscoverer(),
        database_size_discoverer=PostgresDatabaseSizeDiscoverer(),
        database_statistics_discoverer=PostgresDatabaseStatisticsDiscoverer(),
        replication_discoverer=PostgresReplicationDiscoverer(),
        table_statistics_discoverer=PostgresTableStatisticsDiscoverer(),
        index_statistics_discoverer=PostgresIndexStatisticsDiscoverer(),
        connection_statistics_discoverer=PostgresConnectionStatisticsDiscoverer(),
        lock_statistics_discoverer=PostgresLockStatisticsDiscoverer(),
    )

def get_database_metadata_persistence_service(
    session: Session = Depends(
        get_db_session,
    ),
) -> DatabaseMetadataPersistenceService:
    metadata_repository = DatabaseMetadataRepositoryImpl(
        session,
    )

    return DatabaseMetadataPersistenceServiceImpl(
        metadata_repository,
    )