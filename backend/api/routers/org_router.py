from uuid import UUID
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from backend.api.dependencies.auth import get_current_user
from backend.platform.auth.domain.user import User
from backend.api.dependencies import get_organization_service
from backend.platform.organizations.application.organization_service import OrganizationService
from backend.platform.organizations.dto.create_organization_request import CreateOrganizationRequest
from backend.platform.organizations.dto.organization_response import OrganizationResponse
from backend.platform.organizations.dto.update_org_request import UpdateOrganizationRequest


router = APIRouter(
    prefix="/organizations",
)


@router.post(
    "",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_organization(
    request: CreateOrganizationRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> OrganizationResponse:

    return service.create(
        owner_id=current_user.id,
        request=request,
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: UUID,
    current_user: User = Depends(
        get_current_user,
    ),
    service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> OrganizationResponse:
    """
    Returns a single organization.
    """

    return service.get(
        organization_id=organization_id,
        user_id=current_user.id,
    )

@router.get(
    "",
    response_model=list[OrganizationResponse],
)
def list_organizations(
    current_user: User = Depends(
        get_current_user,
    ),
    service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> list[OrganizationResponse]:
    """
    Returns organizations accessible to the current user.
    """

    return service.list(
        current_user.id,
    )

@router.delete(
    "/{organization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> None:
    """
    Delete an organization.
    """

    service.delete(
        organization_id=organization_id,
    )

@router.put(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def update_organization(
    organization_id: UUID,
    request: UpdateOrganizationRequest,
    current_user: User = Depends(
        get_current_user,
    ),
    service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> OrganizationResponse:
    """
    Updates an organization.
    """

    return service.update(
        organization_id=organization_id,
        user_id=current_user.id,
        request=request,
    )