from unittest.mock import Mock
from uuid import uuid4

from backend.platform.projects.application.project_service_impl import (
    ProjectServiceImpl,
)
from backend.platform.projects.dto.create_project_request import (
    CreateProjectRequest,
)
from tests.factorries import (
    create_organization,
    create_project,
)


def test_create_project():
    """
    Projects are created successfully.
    """

    organization = create_organization()

    repository = Mock()

    repository.save.return_value = create_project(
        organization.id,
        name="Backend",
        description="Backend APIs",
    )

    service = ProjectServiceImpl(
        repository,
    )

    response = service.create(
        organization.id,
        CreateProjectRequest(
            name="Backend",
            description="Backend APIs",
        ),
    )

    assert response.name == "Backend"


def test_get_project():
    """
    Projects can be retrieved.
    """

    organization = create_organization()

    project = create_project(
        organization.id,
    )

    repository = Mock()

    repository.get_by_id.return_value = project

    service = ProjectServiceImpl(
        repository,
    )

    response = service.get(
        project.id,
    )

    assert response.id == project.id