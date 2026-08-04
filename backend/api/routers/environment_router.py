from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from backend.platform.environments.dto.update_env_request import UpdateEnvironmentRequest
from backend.api.dependencies import get_environment_service
from backend.platform.environments.application.environment_service import EnvironmentService
from backend.platform.environments.dto.create_environment_request import CreateEnvironmentRequest
from backend.platform.environments.dto.environment_response import EnvironmentResponse


router = APIRouter(
    prefix="/organizations/{organization_id}/projects/{project_id}/environments",
)


@router.post(
    "",
    response_model=EnvironmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_environment(
    organization_id: UUID,
    project_id: UUID,
    request: CreateEnvironmentRequest,
    service: EnvironmentService = Depends(
        get_environment_service,
    ),
) -> EnvironmentResponse:
    """
    Create an environment within a project.
    """

    return service.create(
        project_id=project_id,
        request=request,
    )

@router.get(
    "/{environment_id}",
    response_model=EnvironmentResponse,
)
def get_environment(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    service: EnvironmentService = Depends(
        get_environment_service,
    ),
) -> EnvironmentResponse:
    """
    Retrieve an environment.
    """

    environment = service.get(
        environment_id=environment_id,
    )

    if (
        environment is None
        or environment.project_id != project_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Environment not found",
        )

    return environment

@router.get(
    "",
    response_model=list[EnvironmentResponse],
)
def list_environments(
    organization_id: UUID,
    project_id: UUID,
    service: EnvironmentService = Depends(
        get_environment_service,
    ),
) -> list[EnvironmentResponse]:
    """
    Retrieve all environments belonging to a project.
    """

    return service.list_by_project(
        project_id=project_id,
    )

@router.put(
    "/{environment_id}",
    response_model=EnvironmentResponse,
)
def update_environment(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    request: UpdateEnvironmentRequest,
    service: EnvironmentService = Depends(
        get_environment_service,
    ),
) -> EnvironmentResponse:
    """
    Update an existing environment.
    """

    try:
        return service.update(
            project_id=project_id,
            environment_id=environment_id,
            request=request,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

@router.delete(
    "/{environment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_environment(
    organization_id: UUID,
    project_id: UUID,
    environment_id: UUID,
    service: EnvironmentService = Depends(
        get_environment_service,
    ),
) -> None:
    """
    Delete an environment.
    """

    try:
        service.delete(
            project_id=project_id,
            environment_id=environment_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc