from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from backend.api.dependencies.api_dependencies import get_api_service
from backend.platform.apis.service.api_service import ApiService
from backend.platform.apis.dto.api_response import ApiResponse
from backend.platform.apis.dto.create_api_request import CreateApiRequest
from backend.platform.apis.dto.update_api_request import UpdateApiRequest
from backend.api.dependencies.platform import get_discovery_service
from backend.platform.apis.dto.discover_apis_request import DiscoverApisRequest
from backend.platform.apis.discovery.synchronization.sync_result import SyncResult
from backend.platform.apis.discovery.application.discovery_service import DiscoveryService
from backend.platform.apis.dto.api_endpoint_response import ApiEndpointResponse


router = APIRouter(
    prefix="/organizations/{organization_id}/projects/{project_id}/environments/{environment_id}/apis",
    tags=["APIs"],
)


@router.post(
    "",
    response_model=ApiResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_api(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    request: CreateApiRequest,
    service: ApiService = Depends(
        get_api_service,
    ),
) -> ApiResponse:
    api = service.create(
        environment_id=environment_id,
        request=request,
    )

    return ApiResponse.model_validate(
        api,
    )


@router.get(
    "",
    response_model=list[ApiResponse],
)
def list_apis(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    service: ApiService = Depends(
        get_api_service,
    ),
) -> list[ApiResponse]:
    apis = service.list(
        environment_id,
    )

    return [
        ApiResponse.model_validate(
            api,
        )
        for api in apis
    ]


@router.get(
    "/{api_id}",
    response_model=ApiResponse,
)
def get_api(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    api_id: UUID,
    service: ApiService = Depends(
        get_api_service,
    ),
) -> ApiResponse:
    api = service.get(
        api_id,
    )

    if api is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API not found.",
        )

    return ApiResponse.model_validate(
        api,
    )

@router.get(
    "/{api_id}/endpoints",
    response_model=list[ApiEndpointResponse],
)
def list_api_endpoints(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    api_id: UUID,
    service: ApiService = Depends(
        get_api_service,
    ),
) -> list[ApiEndpointResponse]:
    endpoints = service.list_endpoints(
        api_id,
    )

    return [
        ApiEndpointResponse.model_validate(
            endpoint,
        )
        for endpoint in endpoints
    ]

@router.put(
    "/{api_id}",
    response_model=ApiResponse,
)
def update_api(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    api_id: UUID,
    request: UpdateApiRequest,
    service: ApiService = Depends(
        get_api_service,
    ),
) -> ApiResponse:
    try:
        api = service.update(
            api_id=api_id,
            request=request,
        )
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex),
        )

    return ApiResponse.model_validate(
        api,
    )


@router.delete(
    "/{api_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_api(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    api_id: UUID,
    service: ApiService = Depends(
        get_api_service,
    ),
) -> None:
    service.delete(
        api_id,
    )

@router.post(
    "/{api_id}/discover",
    response_model=SyncResult,
    status_code=status.HTTP_200_OK,
)
def discover_apis(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    api_id: UUID,
    request: DiscoverApisRequest,
    discovery_service: DiscoveryService = Depends(
        get_discovery_service,
    ),
) -> SyncResult:
    """
    Discovers and synchronizes endpoints for a
    specific registered API.
    """

    return discovery_service.discover(
        environment_id=environment_id,
        api_id=api_id,
        request=request,
    )