from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.platform.access_control.domain.org_membership import (
    OrganizationMembership,
)
from backend.platform.access_control.infra.org_membership_model import (
    OrganizationMembershipModel,
)
from backend.platform.access_control.repositories.org_membership_repo import (
    OrganizationMembershipRepository,
)


class OrganizationMembershipRepositoryImpl(
    OrganizationMembershipRepository,
):
    """
    SQLAlchemy implementation of the organization
    membership repository.
    """

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def create(
        self,
        membership: OrganizationMembership,
    ) -> OrganizationMembership:
        model = OrganizationMembershipModel(
            id=membership.id,
            organization_id=membership.organization_id,
            user_id=membership.user_id,
            role=membership.role,
        )

        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)

        return self._to_domain(model)

    def get_by_id(
        self,
        membership_id: UUID,
    ) -> OrganizationMembership | None:
        statement = (
            select(
                OrganizationMembershipModel,
            )
            .where(
                OrganizationMembershipModel.id == membership_id,
            )
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def list_by_organization(
        self,
        organization_id: UUID,
    ) -> list[OrganizationMembership]:
        statement = (
            select(
                OrganizationMembershipModel,
            )
            .where(
                OrganizationMembershipModel.organization_id == organization_id,
            )
        )

        models = self._session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def list_by_user(
        self,
        user_id: UUID,
    ) -> list[OrganizationMembership]:
        statement = (
            select(
                OrganizationMembershipModel,
            )
            .where(
                OrganizationMembershipModel.user_id == user_id,
            )
        )

        models = self._session.scalars(statement).all()

        return [
            self._to_domain(model)
            for model in models
        ]

    def get_membership(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> OrganizationMembership | None:
        statement = (
            select(
                OrganizationMembershipModel,
            )
            .where(
                OrganizationMembershipModel.organization_id == organization_id,
                OrganizationMembershipModel.user_id == user_id,
            )
        )

        model = self._session.scalar(statement)

        if model is None:
            return None

        return self._to_domain(model)

    def delete(
        self,
        membership_id: UUID,
    ) -> None:
        model = self._session.get(
            OrganizationMembershipModel,
            membership_id,
        )

        if model is None:
            return

        self._session.delete(model)
        self._session.commit()

    @staticmethod
    def _to_domain(
        model: OrganizationMembershipModel,
    ) -> OrganizationMembership:
        return OrganizationMembership(
            id=model.id,
            organization_id=model.organization_id,
            user_id=model.user_id,
            role=model.role,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def exists(
        self,
        organization_id: UUID,
        user_id: UUID,
    ) -> bool:
        return (
            self._session.query(
                OrganizationMembershipModel,
            )
            .filter(
                OrganizationMembershipModel.organization_id == organization_id,
                OrganizationMembershipModel.user_id == user_id,
            )
            .first()
            is not None
        )