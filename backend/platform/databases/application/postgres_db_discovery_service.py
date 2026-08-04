import psycopg
from uuid import UUID
from backend.platform.databases.dto.db_discovery_result import DatabaseDiscoveryResult
from backend.platform.databases.dto.db_statistics_result import DatabaseStatisticsResult
from backend.platform.databases.application.db_discovery_service import DatabaseDiscoveryService
from backend.platform.databases.repositories.db_connection_repo import DatabaseConnectionRepository
from backend.platform.databases.application.connection_statistics_discoverer import ConnectionStatisticsDiscoverer
from backend.platform.databases.application.db_settings_discoverer import DatabaseSettingsDiscoverer
from backend.platform.databases.application.db_size_discoverer import DatabaseSizeDiscoverer
from backend.platform.databases.application.db_statistics_discoverer import DatabaseStatisticsDiscoverer
from backend.platform.databases.application.extension_discoverer import ExtensionDiscoverer
from backend.platform.databases.application.function_discoverer import FunctionDiscoverer
from backend.platform.databases.application.index_discoverer import IndexDiscoverer
from backend.platform.databases.application.index_statistics_discoverer import IndexStatisticsDiscoverer
from backend.platform.databases.application.lock_statistics_discoverer import LockStatisticsDiscoverer
from backend.platform.databases.application.replication_discoverer import ReplicationDiscoverer
from backend.platform.databases.application.schema_discoverer import SchemaDiscoverer
from backend.platform.databases.application.sequence_discoverer import SequenceDiscoverer
from backend.platform.databases.application.table_discoverer import TableDiscoverer
from backend.platform.databases.application.table_statistics_discoverer import TableStatisticsDiscoverer
from backend.platform.databases.application.trigger_discoverer import TriggerDiscoverer
from backend.platform.databases.application.version_discoverer import VersionDiscoverer
from backend.platform.databases.application.view_discoverer import ViewDiscoverer
from backend.platform.databases.repositories.db_connection_repo import DatabaseConnectionRepository
from backend.platform.databases.application.column_discoverer import ColumnDiscoverer
from backend.platform.databases.application.constraint_discoverer import ConstraintDiscoverer



class PostgresDatabaseDiscoveryService(
    DatabaseDiscoveryService,
):
    """
    PostgreSQL implementation of the discovery service.
    """

    def __init__(
        self,
        repository: DatabaseConnectionRepository,
        version_discoverer: VersionDiscoverer,
        schema_discoverer: SchemaDiscoverer,
        extension_discoverer: ExtensionDiscoverer,
        table_discoverer: TableDiscoverer,
        column_discoverer: ColumnDiscoverer,
        constraint_discoverer: ConstraintDiscoverer,
        view_discoverer: ViewDiscoverer,
        function_discoverer: FunctionDiscoverer,
        index_discoverer: IndexDiscoverer,
        trigger_discoverer: TriggerDiscoverer,
        sequence_discoverer: SequenceDiscoverer,
        database_settings_discoverer: DatabaseSettingsDiscoverer,
        database_size_discoverer: DatabaseSizeDiscoverer,
        database_statistics_discoverer: DatabaseStatisticsDiscoverer,
        replication_discoverer: ReplicationDiscoverer,
        table_statistics_discoverer: TableStatisticsDiscoverer,
        index_statistics_discoverer: IndexStatisticsDiscoverer,
        connection_statistics_discoverer: ConnectionStatisticsDiscoverer,
        lock_statistics_discoverer: LockStatisticsDiscoverer,
    ):
        self._repository = repository

        self._version_discoverer = version_discoverer
        self._schema_discoverer = schema_discoverer
        self._extension_discoverer = extension_discoverer
        self._table_discoverer = table_discoverer
        self._column_discoverer = column_discoverer
        self._constraint_discoverer = constraint_discoverer
        self._view_discoverer = view_discoverer
        self._function_discoverer = function_discoverer
        self._index_discoverer = index_discoverer
        self._trigger_discoverer = trigger_discoverer
        self._sequence_discoverer = sequence_discoverer

        self._database_settings_discoverer = database_settings_discoverer
        self._database_size_discoverer = database_size_discoverer
        self._database_statistics_discoverer = (
            database_statistics_discoverer
        )
        self._replication_discoverer = replication_discoverer

        self._table_statistics_discoverer = (
            table_statistics_discoverer
        )
        self._index_statistics_discoverer = (
            index_statistics_discoverer
        )
        self._connection_statistics_discoverer = (
            connection_statistics_discoverer
        )
        self._lock_statistics_discoverer = (
            lock_statistics_discoverer
        )

    def discover(
        self,
        connection_id: UUID,
    ) -> DatabaseDiscoveryResult:
        connection = self._repository.get_by_id(
            connection_id,
        )

        if connection is None:
            raise ValueError(
                "Database connection not found.",
            )

        db = None

        try:
            db = psycopg.connect(
                host=connection.host,
                port=connection.port,
                dbname=connection.database_name,
                user=connection.username,
                password=connection.password,
                sslmode=(
                    "require"
                    if connection.ssl_enabled
                    else "prefer"
                ),
            )

            version = self._version_discoverer.discover(db)

            schemas = self._schema_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            extensions = self._extension_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            tables = self._table_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            columns = self._column_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            constraints = self._constraint_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            views = self._view_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            functions = self._function_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            indexes = self._index_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            triggers = self._trigger_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            sequences = self._sequence_discoverer.discover(
                connection=db,
                connection_id=connection.id,
            )

            settings = (
                self._database_settings_discoverer.discover(
                    db,
                )
            )

            database_size = (
                self._database_size_discoverer.discover(
                    db,
                )
            )

            database_statistics = (
                self._database_statistics_discoverer.discover(
                    db,
                )
            )

            replication = (
                self._replication_discoverer.discover(
                    db,
                )
            )

            table_statistics = (
                self._table_statistics_discoverer.discover(
                    db,
                )
            )

            index_statistics = (
                self._index_statistics_discoverer.discover(
                    db,
                )
            )

            connection_statistics = (
                self._connection_statistics_discoverer.discover(
                    db,
                )
            )

            lock_statistics = (
                self._lock_statistics_discoverer.discover(
                    db,
                )
            )

            return DatabaseDiscoveryResult(
                postgres_version=version,
                schemas=schemas,
                tables=tables,
                columns=columns,
                constraints=constraints,
                views=views,
                functions=functions,
                indexes=indexes,
                triggers=triggers,
                sequences=sequences,
                extensions=extensions,
                database_size=database_size,
                settings=settings,
                replication=replication,
                database_statistics=DatabaseStatisticsResult(
                    **database_statistics,
                ),
                table_statistics=table_statistics,
                index_statistics=index_statistics,
                connection_statistics=connection_statistics,
                lock_statistics=lock_statistics,
            )

        finally:
            if db is not None:
                db.close()