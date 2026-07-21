from uuid import uuid4

import pytest

from backend.platform.projects.infra.project_model import (
    ProjectModel,
)


@pytest.fixture
def project(
    db_session,
    organization,
) -> ProjectModel:
    project = ProjectModel(
        id=uuid4(),
        organization_id=organization.id,
        name="Test Project",
        description="Repository Test Project",
    )

    db_session.add(
        project,
    )
    db_session.commit()
    db_session.refresh(
        project,
    )

    return project