from unittest.mock import Mock

from backend.platform.environments.application.environment_service_impl import (
    EnvironmentServiceImpl,
)
from backend.platform.environments.dto.create_environment_request import (
    CreateEnvironmentRequest,
)
from tests.factorries import (
    create_environment,
    create_project,
    create_organization,
)


def test_create_environment():
    """
    Environments are created successfully.
    """

    organization = create_organization()

    project = create_project(
        organization.id,
    )

    repository = Mock()

    repository.save.return_value = create_environment(
        project.id,
        name="Development",
        description="Development environment",
    )

    service = EnvironmentServiceImpl(
        repository,
    )

    response = service.create(
        project.id,
        CreateEnvironmentRequest(
            name="Development",
            description="Development environment",
        ),
    )

    assert response.name == "Development"


def test_get_environment():
    """
    Environments can be retrieved.
    """

    organization = create_organization()

    project = create_project(
        organization.id,
    )

    environment = create_environment(
        project.id,
    )

    repository = Mock()

    repository.get_by_id.return_value = environment

    service = EnvironmentServiceImpl(
        repository,
    )

    response = service.get(
        environment.id,
    )

    assert response.id == environment.id