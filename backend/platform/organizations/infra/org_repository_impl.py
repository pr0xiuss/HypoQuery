from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.platform.organizations.domain.organization import Organization
from backend.platform.organizations.infra.organization_model import (
    OrganizationModel,
)
from backend.platform.organizations.repositories.organization_repository import (
    OrganizationRepository,
)


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
            slug=organization.slug,
            created_at=organization.created_at,
            updated_at=organization.updated_at,
        )

        try:
            merged_model = self._session.merge(model)
            self._session.commit()
            self._session.refresh(merged_model)

        except:
            self._session.rollback()
            raise
        
        return self._to_domain(merged_model)

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
            slug=model.slug,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )