from datetime import UTC, datetime
from uuid import UUID
from uuid import uuid4
from backend.platform.shared.database import SessionLocal
from backend.platform.organizations.infra.org_repository_impl import OrganizationRepositoryImpl
from backend.platform.access_control.infra.org_membership_repo_impl import OrganizationMembershipRepositoryImpl
from backend.platform.access_control.application.access_control_service_impl import AccessControlServiceImpl
from backend.platform.shared.transactions.sqlalchemy_transaction_manager import SQLAlchemyTransactionManager
from backend.platform.organizations.application.organization_service import OrganizationService
from backend.platform.organizations.domain.organization import Organization
from backend.platform.organizations.dto.create_organization_request import CreateOrganizationRequest
from backend.platform.organizations.dto.organization_response import OrganizationResponse
from backend.platform.organizations.repositories.organization_repository import OrganizationRepository
from backend.platform.shared.slug import generate_slug
from backend.platform.shared.exceptions.resource import ResourceAlreadyExistsError
from backend.platform.organizations.dto.update_org_request import UpdateOrganizationRequest
from backend.platform.access_control.domain.org_role import OrganizationRole
from backend.platform.access_control.domain.org_membership import OrganizationMembership
from backend.platform.shared.exceptions import ResourceNotFoundError
from backend.platform.access_control.application.access_control_service import AccessControlService
from backend.platform.shared.transactions.transaction_manager import TransactionManager


class OrganizationServiceImpl(OrganizationService):
    """
    Default implementation of the organization application service.
    """

    def __init__(
        self,
        organization_repository: OrganizationRepository,
        access_control_service: AccessControlService,
        transaction_manager: TransactionManager,
    ) -> None:
        self._organization_repository = organization_repository
        self._access_control_service = access_control_service
        self._transaction_manager = transaction_manager

    def create(
        self,
        owner_id: UUID,
        request: CreateOrganizationRequest,
    ) -> OrganizationResponse:
        now = datetime.now(
            UTC,
        )

        slug = generate_slug(
            request.name,
        )

        existing = self._organization_repository.get_by_slug(
            slug,
        )

        if existing is not None:
            raise ResourceAlreadyExistsError(
                "An organization with this name already exists.",
                slug,
            )

        organization = Organization(
            id=uuid4(),
            name=request.name,
            description=request.description,
            slug=slug,
            created_at=now,
            updated_at=now,
        )

        with SessionLocal() as session:

            organization_repository = OrganizationRepositoryImpl(
                session=session,
            )

            membership_repository = OrganizationMembershipRepositoryImpl(
                session=session,
            )

            access_control_service = AccessControlServiceImpl(
                repository=membership_repository,
            )

            transaction_manager = SQLAlchemyTransactionManager(
                session=session,
            )

            try:
                persisted_organization = (
                    organization_repository.save(
                        organization,
                    )
                )

                access_control_service.create_owner_membership(
                    organization_id=persisted_organization.id,
                    user_id=owner_id,
                )

                transaction_manager.commit()

            except Exception:
                transaction_manager.rollback()
                raise

        return OrganizationResponse(
            id=persisted_organization.id,
            name=persisted_organization.name,
            description=persisted_organization.description,
            slug=persisted_organization.slug,
            created_at=persisted_organization.created_at,
            updated_at=persisted_organization.updated_at,
        )

    def get(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> OrganizationResponse:
        with SessionLocal() as session:

            membership_repository = OrganizationMembershipRepositoryImpl(
                session=session,
            )

            access_control_service = AccessControlServiceImpl(
                repository=membership_repository,
            )

            access_control_service.ensure_organization_access(
                organization_id=organization_id,
                user_id=user_id,
            )

        organization = self._organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise ResourceNotFoundError(
                "Organization",
                str(organization_id),
            )

        return OrganizationResponse(
            id=organization.id,
            name=organization.name,
            description=organization.description,
            slug=organization.slug,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
        )

    def list(
        self,
        user_id: UUID,
    ) -> list[OrganizationResponse]:
        organizations = (
            self._organization_repository.list_accessible_to_user(
                user_id,
            )
        )

        return [
            OrganizationResponse(
                id=organization.id,
                name=organization.name,
                description=organization.description,
                slug=organization.slug,
                created_at=organization.created_at,
                updated_at=organization.updated_at,
            )
            for organization in organizations
        ]

    def delete(
        self,
        organization_id: UUID,
    ) -> None:
        self._organization_repository.delete(
            organization_id,
        )

    def update(
        self,
        organization_id: UUID,
        user_id: UUID,
        request: UpdateOrganizationRequest,
    ) -> OrganizationResponse:

        with SessionLocal() as session:

            membership_repository = OrganizationMembershipRepositoryImpl(
                session=session,
            )

            access_control_service = AccessControlServiceImpl(
                repository=membership_repository,
            )

            access_control_service.ensure_organization_access(
                organization_id=organization_id,
                user_id=user_id,
            )

        organization = self._organization_repository.get_by_id(
            organization_id,
        )

        if organization is None:
            raise ResourceNotFoundError(
                "Organization",
                str(organization_id),
            )

        updated_organization = Organization(
            id=organization.id,
            name=request.name,
            description=request.description,
            slug=organization.slug,
            created_at=organization.created_at,
            updated_at=datetime.now(
                UTC,
            ),
        )

        updated = self._organization_repository.update(
            updated_organization,
        )

        return OrganizationResponse(
            id=updated.id,
            name=updated.name,
            description=updated.description,
            slug=updated.slug,
            created_at=updated.created_at,
            updated_at=updated.updated_at,
        )