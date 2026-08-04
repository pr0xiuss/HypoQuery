from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from backend.api.dependencies.api_dependencies import get_api_service
from backend.platform.apis.service.api_service import ApiService
from backend.platform.apis.dto.api_response import ApiResponse
from backend.platform.apis.dto.create_api_request import CreateApiRequest
from backend.platform.apis.dto.update_api_request import UpdateApiRequest


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