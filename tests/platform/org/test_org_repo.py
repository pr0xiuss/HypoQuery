from sqlalchemy.orm import Session

from backend.platform.organizations.infra.org_repository_impl import (
    OrganizationRepositoryImpl,
)
from tests.factorries import create_organization


def test_save_organization(
    db_session: Session,
):
    """
    Organizations can be persisted.
    """

    repository = OrganizationRepositoryImpl(
        db_session,
    )

    organization = create_organization()

    saved = repository.save(
        organization,
    )

    assert saved.id == organization.id


def test_get_organization_by_id(
    db_session: Session,
):
    """
    Organizations can be retrieved by id.
    """

    repository = OrganizationRepositoryImpl(
        db_session,
    )

    organization = repository.save(
        create_organization(),
    )

    loaded = repository.get_by_id(
        organization.id,
    )

    assert loaded is not None
    assert loaded.id == organization.id
    assert loaded.name == organization.name