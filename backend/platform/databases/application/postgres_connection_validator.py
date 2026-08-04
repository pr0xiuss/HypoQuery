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
            print("Validator request:", request)
            print("Host:", request.host)
            print("Port:", request.port)
            print("Database:", request.database_name)
            print("Username:", request.username)
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
            print(request)
            print(request.host)
            print(request.port)
            print(request.database_name)

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT 1",
                )

        finally:
            if connection is not None:
                connection.close()