import psycopg

from backend.platform.databases.application.db_connection_validator import (
    DatabaseConnectionValidator,
)
from backend.platform.databases.dto.create_db_connection_request import (
    CreateDatabaseConnectionRequest,
)


class PostgresConnectionValidator(
    DatabaseConnectionValidator,
):
    """
    Validates PostgreSQL database connectivity.
    """

    def validate(
        self,
        request: CreateDatabaseConnectionRequest,
    ) -> None:
        connection = None

        try:
            connection = psycopg.connect(
                host=request.host,
                port=request.port,
                dbname=request.database_name,
                user=request.username,
                password=request.password,
                sslmode=(
                    "require"
                    if request.ssl_enabled
                    else "prefer"
                ),
                connect_timeout=5,
            )

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1",
                )

        finally:
            if connection is not None:
                connection.close()