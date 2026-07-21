from datetime import UTC
from datetime import datetime
from uuid import UUID
from uuid import uuid4
from backend.platform.databases.application.db_connection_validator import DatabaseConnectionValidator
from backend.platform.databases.application.db_connection_service import DatabaseConnectionService
from backend.platform.databases.domain.db_connection import DatabaseConnection
from backend.platform.databases.dto.create_db_connection_request import CreateDatabaseConnectionRequest
from backend.platform.databases.dto.db_connection_response import DatabaseConnectionResponse
from backend.platform.databases.repositories.db_connection_repo import DatabaseConnectionRepository
from backend.platform.databases.application.db_discovery_service import DatabaseDiscoveryService
from backend.platform.databases.dto.db_health_result import DatabaseHealthResult
from backend.platform.databases.application.db_health_service import DatabaseHealthService
from backend.platform.databases.application.db_metadata_persistence_service import DatabaseMetadataPersistenceService
from backend.platform.databases.application.db_discovery_service import DatabaseDiscoveryService


class DatabaseConnectionServiceImpl(
    DatabaseConnectionService,
):
    """
    Default implementation of the database connection service.
    """

    def __init__(
        self,
        repository: DatabaseConnectionRepository,
        validator: DatabaseConnectionValidator,
        discovery_service: DatabaseDiscoveryService,
        metadata_persistence_service: DatabaseMetadataPersistenceService,
        health_service: DatabaseHealthService,
    ):
        self._repository = repository
        self._validator = validator
        self._discovery_service = discovery_service
        self._metadata_persistence_service = metadata_persistence_service
        self._health_service = health_service

    def create(
        self,
        environment_id: UUID,
        request: CreateDatabaseConnectionRequest,
    ) -> DatabaseConnectionResponse:
        now = datetime.now(
            UTC,
        )

        connection = DatabaseConnection(
            id=uuid4(),
            environment_id=environment_id,
            name=request.name,
            host=request.host,
            port=request.port,
            database_name=request.database_name,
            username=request.username,
            password=request.password,
            ssl_enabled=request.ssl_enabled,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        self._validator.validate(
            request,
        )

        saved_connection = self._repository.save(
            connection,
        )

        self.refresh_metadata(
            saved_connection.id,
        )

        return saved_connection

    def get(
        self,
        connection_id: UUID,
    ) -> DatabaseConnectionResponse | None:
        connection = self._repository.get_by_id(
            connection_id,
        )

        if connection is None:
            return None

        return DatabaseConnectionResponse(
            id=connection.id,
            environment_id=connection.environment_id,
            name=connection.name,
            host=connection.host,
            port=connection.port,
            database_name=connection.database_name,
            username=connection.username,
            ssl_enabled=connection.ssl_enabled,
            is_active=connection.is_active,
            created_at=connection.created_at,
            updated_at=connection.updated_at,
        )

    def list(
        self,
        environment_id: UUID,
    ) -> list[DatabaseConnectionResponse]:
        connections = self._repository.list_by_environment(
            environment_id,
        )

        return [
            DatabaseConnectionResponse(
                id=connection.id,
                environment_id=connection.environment_id,
                name=connection.name,
                host=connection.host,
                port=connection.port,
                database_name=connection.database_name,
                username=connection.username,
                ssl_enabled=connection.ssl_enabled,
                is_active=connection.is_active,
                created_at=connection.created_at,
                updated_at=connection.updated_at,
            )
            for connection in connections
        ]

    def delete(
        self,
        connection_id: UUID,
    ) -> None:
        self._repository.delete(
            connection_id,
        )

    def refresh_metadata(
        self,
        connection_id: UUID,
    ) -> None:
        discovery_result = self._discovery_service.discover(
            connection_id,
        )

        self._metadata_persistence_service.refresh(
            connection_id,
            discovery_result,
        )

    def check_health(
        self,
        connection_id: UUID,
    ) -> DatabaseHealthResult:
        return self._health_service.check_health(
            connection_id,
        )