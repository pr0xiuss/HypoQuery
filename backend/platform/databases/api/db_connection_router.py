from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from backend.api.dependencies import (
    get_database_connection_service,
)
from backend.platform.databases.application.db_connection_service import (
    DatabaseConnectionService,
)
from backend.platform.databases.dto.create_db_connection_request import (
    CreateDatabaseConnectionRequest,
)
from backend.platform.databases.dto.db_connection_response import (
    DatabaseConnectionResponse,
)

router = APIRouter()


@router.post(
    "/environments/{environment_id}/database-connections",
    response_model=DatabaseConnectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_database_connection(
    environment_id: UUID,
    request: CreateDatabaseConnectionRequest,
    service: DatabaseConnectionService = Depends(
        get_database_connection_service,
    ),
) -> DatabaseConnectionResponse:
    """
    Register a PostgreSQL database connection.
    """

    connection = service.create(
        environment_id=environment_id,
        request=request,
    )

    return DatabaseConnectionResponse.model_validate(
        connection,
    )


@router.get(
    "/database-connections/{connection_id}",
    response_model=DatabaseConnectionResponse,
)
def get_database_connection(
    connection_id: UUID,
    service: DatabaseConnectionService = Depends(
        get_database_connection_service,
    ),
) -> DatabaseConnectionResponse:
    """
    Retrieve a database connection.
    """

    connection = service.get(
        connection_id,
    )

    if connection is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database connection not found.",
        )

    return DatabaseConnectionResponse.model_validate(
        connection,
    )


@router.get(
    "/environments/{environment_id}/database-connections",
    response_model=list[DatabaseConnectionResponse],
)
def list_database_connections(
    environment_id: UUID,
    service: DatabaseConnectionService = Depends(
        get_database_connection_service,
    ),
) -> list[DatabaseConnectionResponse]:
    """
    List all database connections for an environment.
    """

    connections = service.list(
        environment_id,
    )

    return [
        DatabaseConnectionResponse.model_validate(
            connection,
        )
        for connection in connections
    ]


@router.delete(
    "/database-connections/{connection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_database_connection(
    connection_id: UUID,
    service: DatabaseConnectionService = Depends(
        get_database_connection_service,
    ),
) -> None:
    """
    Delete a database connection.
    """

    service.delete(
        connection_id,
    )