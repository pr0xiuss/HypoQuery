from backend.platform.projects.infra.project_repository_impl import ProjectRepositoryImpl
from backend.platform.organizations.infra.org_repository_impl import OrganizationRepositoryImpl
from tests.factories import (
    create_organization,
    create_project,
)


def test_save_project(
    db_session,
):
    """
    Projects can be persisted.
    """
    
    organization = create_organization()

    org_repository = OrganizationRepositoryImpl(
        db_session,
    )

    organization = org_repository.save(
        organization,
    )

    repository = ProjectRepositoryImpl(
        db_session,
    )

    project = create_project(
        organization.id,
    )

    saved = repository.save(
        project,
    )

    assert saved.id == project.id


def test_get_project_by_id(
    db_session,
):
    """
    Projects can be retrieved by id.
    """
    
    organization = OrganizationRepositoryImpl(
        db_session,
    ).save(
        create_organization(),
    )

    repository = ProjectRepositoryImpl(
        db_session,
    )


    project = repository.save(
        create_project(
            organization.id,
        )
    )

    loaded = repository.get_by_id(
        project.id,
    )

    assert loaded is not None
    assert loaded.id == project.id