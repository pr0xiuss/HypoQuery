from uuid import uuid4

import pytest

from backend.platform.organizations.infra.organization_model import (
    OrganizationModel,
)


@pytest.fixture
def organization(
    db_session,
) -> OrganizationModel:
    organization = OrganizationModel(
        id=uuid4(),
        name="Test Organization",
        slug=f"test-org-{uuid4().hex[:8]}",
    )

    db_session.add(
        organization,
    )
    db_session.commit()
    db_session.refresh(
        organization,
    )

    return organization