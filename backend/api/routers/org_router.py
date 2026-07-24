from uuid import UUID
from fastapi import HTTPException
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

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
    service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> OrganizationResponse:
    """
    Create a new organization.
    """

    owner_id = UUID("00000000-0000-0000-0000-000000000001")

    return service.create(
        owner_id=owner_id,
        request=request,
    )


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> OrganizationResponse:
    """
    Retrieve an organization by ID.
    """

    organization = service.get(
        organization_id,
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found.",
        )

    return organization

@router.get(
    "",
    response_model=list[OrganizationResponse],
)
def list_organizations(
    service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> list[OrganizationResponse]:
    """
    Retrieve all organizations visible to the current user.
    """

    return service.list()

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
    status_code=status.HTTP_200_OK,
)
def update_organization(
    organization_id: UUID,
    request: UpdateOrganizationRequest,
    service: OrganizationService = Depends(
        get_organization_service,
    ),
) -> OrganizationResponse:
    """
    Update an organization.
    """

    organization = service.update(
        organization_id=organization_id,
        request=request,
    )

    if organization is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return organization