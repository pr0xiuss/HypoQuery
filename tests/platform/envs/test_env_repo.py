from backend.platform.environments.infra.environment_repository_impl import (
    EnvironmentRepositoryImpl,
)
from backend.platform.organizations.infra.org_repository_impl import (
    OrganizationRepositoryImpl,
)
from backend.platform.projects.infra.project_repository_impl import (
    ProjectRepositoryImpl,
)
from tests.factories import (
    create_environment,
    create_organization,
    create_project,
)


def test_save_environment(
    db_session,
):
    """
    Environments can be persisted.
    """

    organization = OrganizationRepositoryImpl(
        db_session,
    ).save(
        create_organization(),
    )

    project = ProjectRepositoryImpl(
        db_session,
    ).save(
        create_project(
            organization.id,
        ),
    )

    repository = EnvironmentRepositoryImpl(
        db_session,
    )

    environment = create_environment(
        project.id,
    )

    saved = repository.save(
        environment,
    )

    assert saved.id == environment.id


def test_get_environment_by_id(
    db_session,
):
    """
    Environments can be retrieved.
    """

    organization = OrganizationRepositoryImpl(
        db_session,
    ).save(
        create_organization(),
    )

    project = ProjectRepositoryImpl(
        db_session,
    ).save(
        create_project(
            organization.id,
        ),
    )

    repository = EnvironmentRepositoryImpl(
        db_session,
    )

    environment = repository.save(
        create_environment(
            project.id,
        )
    )

    loaded = repository.get_by_id(
        environment.id,
    )

    assert loaded is not None
    assert loaded.id == environment.id