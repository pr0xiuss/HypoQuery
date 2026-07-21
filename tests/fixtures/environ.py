from uuid import uuid4

import pytest

from backend.platform.environments.infra.environment_model import (
    EnvironmentModel,
)


@pytest.fixture
def environment(
    db_session,
    project,
) -> EnvironmentModel:
    environment = EnvironmentModel(
        id=uuid4(),
        project_id=project.id,
        name="Development",
        description="Repository Test Environment",
    )

    db_session.add(
        environment,
    )
    db_session.commit()
    db_session.refresh(
        environment,
    )

    return environment