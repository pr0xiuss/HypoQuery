from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from backend.api.dependencies.api_dependencies import get_database_explorer_service
from backend.platform.databases.application.db_explorer_service import DatabaseExplorerService
from backend.platform.databases.api.responses.schema_summary_response import SchemaSummaryResponse
from backend.platform.databases.api.responses.table_summary_response import TableSummaryResponse
from backend.api.dependencies import get_database_connection_service
from backend.platform.databases.api.responses.table_detail_response import TableDetailResponse
from backend.platform.databases.application.db_connection_service import DatabaseConnectionService
from backend.platform.databases.dto.create_db_connection_request import CreateDatabaseConnectionRequest
from backend.platform.databases.dto.update_db_connection_request import UpdateDatabaseConnectionRequest
from backend.platform.databases.dto.db_connection_response import DatabaseConnectionResponse
from backend.platform.databases.dto.db_health_response import DatabaseHealthResponse
from backend.platform.databases.dto.refresh_db_metadata_response import RefreshDatabaseMetadataResponse
from backend.platform.databases.dto.db_overview_response import DatabaseOverviewResponse
from backend.platform.databases.api.responses.extension_summary_response import ExtensionSummaryResponse
from backend.platform.databases.api.responses.function_summary_response import FunctionSummaryResponse
from backend.platform.databases.api.responses.index_summary_response import IndexSummaryResponse
from backend.platform.databases.api.responses.sequence_summary_response import SequenceSummaryResponse
from backend.platform.databases.api.responses.trigger_summary_response import TriggerSummaryResponse
from backend.platform.databases.api.responses.view_summary_response import ViewSummaryResponse


router = APIRouter(
    prefix="/organizations/{organization_id}/projects/{project_id}/environments/{environment_id}/database-connections",
    tags=["Database Connections"],
)


@router.post(
    "",
    response_model=DatabaseConnectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_database_connection(
    organization_id: UUID,
    project_id: UUID,
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
    "",
    response_model=list[DatabaseConnectionResponse],
)
def list_database_connections(
    organization_id: UUID,
    project_id: UUID,
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


@router.get(
    "/{connection_id}",
    response_model=DatabaseConnectionResponse,
)
def get_database_connection(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
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


@router.put(
    "/{connection_id}",
    response_model=DatabaseConnectionResponse,
)
def update_database_connection(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    request: UpdateDatabaseConnectionRequest,
    service: DatabaseConnectionService = Depends(
        get_database_connection_service,
    ),
) -> DatabaseConnectionResponse:
    """
    Update a PostgreSQL database connection.
    """
    print("update point hit")

    try:
        connection = service.update(
            connection_id=connection_id,
            request=request,
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database connection not found.",
        )

    return DatabaseConnectionResponse.model_validate(
        connection,
    )


@router.delete(
    "/{connection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_database_connection(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
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


@router.post(
    "/{connection_id}/refresh",
    response_model=RefreshDatabaseMetadataResponse,
)
def refresh_metadata(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseConnectionService = Depends(
        get_database_connection_service,
    ),
) -> RefreshDatabaseMetadataResponse:
    service.refresh_metadata(
        connection_id,
    )

    return RefreshDatabaseMetadataResponse(
        message="Database metadata refreshed successfully.",
    )


@router.get(
    "/{connection_id}/health",
    response_model=DatabaseHealthResponse,
)
def check_health(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseConnectionService = Depends(
        get_database_connection_service,
    ),
) -> DatabaseHealthResponse:
    result = service.check_health(
        connection_id,
    )

    return DatabaseHealthResponse(
        healthy=result.healthy,
        latency_ms=result.latency_ms,
        postgres_version=result.postgres_version,
        checked_at=result.checked_at,
        error=result.error,
    )

@router.get(
    "/{connection_id}/overview",
    response_model=DatabaseOverviewResponse,
)
def get_database_overview(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseConnectionService = Depends(
        get_database_connection_service,
    ),
) -> DatabaseOverviewResponse:
    try:
        return service.get_overview(
            connection_id,
        )
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex),
        )

@router.get(
    "/{connection_id}/schemas",
    response_model=list[SchemaSummaryResponse],
)
def get_schemas(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseExplorerService = Depends(
        get_database_explorer_service,
    ),
) -> list[SchemaSummaryResponse]:
    return service.get_schemas(
        connection_id,
    )

@router.get(
    "/{connection_id}/tables",
    response_model=list[TableSummaryResponse],
)
def get_tables(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseExplorerService = Depends(
        get_database_explorer_service,
    ),
) -> list[TableSummaryResponse]:
    return service.get_tables(
        connection_id,
    )

@router.get(
    "/{connection_id}/views",
    response_model=list[ViewSummaryResponse],
)
def get_views(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseExplorerService = Depends(
        get_database_explorer_service,
    ),
) -> list[ViewSummaryResponse]:
    return service.get_views(
        connection_id,
    )

@router.get(
    "/{connection_id}/functions",
    response_model=list[FunctionSummaryResponse],
)
def get_functions(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseExplorerService = Depends(
        get_database_explorer_service,
    ),
) -> list[FunctionSummaryResponse]:
    return service.get_functions(
        connection_id,
    )

@router.get(
    "/{connection_id}/indexes",
    response_model=list[IndexSummaryResponse],
)
def get_indexes(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseExplorerService = Depends(
        get_database_explorer_service,
    ),
) -> list[IndexSummaryResponse]:
    return service.get_indexes(
        connection_id,
    )

@router.get(
    "/{connection_id}/triggers",
    response_model=list[TriggerSummaryResponse],
)
def get_triggers(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseExplorerService = Depends(
        get_database_explorer_service,
    ),
) -> list[TriggerSummaryResponse]:
    return service.get_triggers(
        connection_id,
    )

@router.get(
    "/{connection_id}/sequences",
    response_model=list[SequenceSummaryResponse],
)
def get_sequences(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseExplorerService = Depends(
        get_database_explorer_service,
    ),
) -> list[SequenceSummaryResponse]:
    return service.get_sequences(
        connection_id,
    )

@router.get(
    "/{connection_id}/extensions",
    response_model=list[ExtensionSummaryResponse],
)
def get_extensions(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    service: DatabaseExplorerService = Depends(
        get_database_explorer_service,
    ),
) -> list[ExtensionSummaryResponse]:
    return service.get_extensions(
        connection_id,
    )

@router.get(
    "/{connection_id}/tables/{schema_name}/{table_name}",
    response_model=TableDetailResponse,
)
def get_table(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    connection_id: UUID,
    schema_name: str,
    table_name: str,
    service: DatabaseExplorerService = Depends(
        get_database_explorer_service,
    ),
) -> TableDetailResponse:
    return service.get_table(
        connection_id=connection_id,
        schema_name=schema_name,
        table_name=table_name,
        
    )                                                                           