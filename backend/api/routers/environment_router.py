from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from backend.api.dependencies import get_environment_service
from backend.platform.environments.application.environment_service import (
    EnvironmentService,
)
from backend.platform.environments.dto.create_environment_request import (
    CreateEnvironmentRequest,
)
from backend.platform.environments.dto.environment_response import (
    EnvironmentResponse,
)

router = APIRouter(
    prefix="/projects/{project_id}/environments",
)


@router.post(
    "",
    response_model=EnvironmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_environment(
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