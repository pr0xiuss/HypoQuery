from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.platform.organizations.domain.organization import Organization
from backend.platform.organizations.infra.organization_model import OrganizationModel
from backend.platform.organizations.repositories.organization_repository import OrganizationRepository
from backend.platform.access_control.infra.org_membership_model import OrganizationMembershipModel

class OrganizationRepositoryImpl(OrganizationRepository):
    """
    SQLAlchemy implementation of the organization repository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def save(
        self,
        organization: Organization,
    ) -> Organization:
        model = OrganizationModel(
            id=organization.id,
            name=organization.name,
            description=organization.description,
            slug=organization.slug,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
        )

        merged_model = self._session.merge(
            model,
        )

        self._session.flush()

        self._session.refresh(
            merged_model,
        )

        return self._to_domain(
            merged_model,
        )

    def get_by_id(
        self,
        organization_id: UUID,
    ) -> Organization | None:
        model = self._session.get(
            OrganizationModel,
            organization_id,
        )

        if model is None:
            return None

        return self._to_domain(model)

    def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        statement = select(OrganizationModel).where(
            OrganizationModel.slug == slug,
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def list_all(
        self,
    ) -> list[Organization]:
        statement = select(OrganizationModel)

        models = self._session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    @staticmethod
    def _to_domain(
        model: OrganizationModel,
    ) -> Organization:
        return Organization(
            id=model.id,
            name=model.name,
            description=model.description,
            slug=model.slug,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def delete(
        self,
        organization_id: UUID,
    ) -> None:
        model = self._session.get(
            OrganizationModel,
            organization_id,
        )

        if model is None:
            return

        try:
            self._session.delete(model)
            self._session.commit()

        except:
            self._session.rollback()
            raise

    def update(
        self,
        organization: Organization,
    ) -> Organization:
        model = self._session.get(
            OrganizationModel,
            organization.id,
        )

        if model is None:
            raise ValueError(
                "Organization not found",
            )

        model.name = organization.name
        model.description = organization.description
        model.slug = organization.slug
        model.updated_at = organization.updated_at

        self._session.commit()
        self._session.refresh(model)

        return self._to_domain(model)

    def list_accessible_to_user(
        self,
        user_id: UUID,
    ) -> list[Organization]:
        models = (
            self._session.query(
                OrganizationModel,
            )
            .join(
                OrganizationMembershipModel,
                OrganizationMembershipModel.organization_id
                == OrganizationModel.id,
            )
            .filter(
                OrganizationMembershipModel.user_id == user_id,
            )
            .order_by(
                OrganizationModel.created_at.desc(),
            )
            .all()
        )

        return [
            self._to_domain(
                model,
            )
            for model in models
        ]