from unittest.mock import Mock
import pytest
from uuid import uuid4
from backend.platform.organizations.application.org_service_imp import (
    OrganizationServiceImpl,
)
from backend.platform.organizations.dto.create_organization_request import (
    CreateOrganizationRequest,
)
from tests.factorries import create_organization


def test_create_organization():
    """
    Organizations are created successfully.
    """

    repository = Mock()
    repository.get_by_slug.return_value = None
    repository.save.return_value = create_organization()

    service = OrganizationServiceImpl(
        repository,
    )

    owner_id = uuid4()

    response = service.create(
        owner_id,
        CreateOrganizationRequest(
            name="Acme",
        ),
    )

    assert response.name.startswith("Acme")



def test_get_organization():
    """
    Organizations can be retrieved.
    """

    organization = create_organization()

    repository = Mock()

    repository.get_by_id.return_value = organization

    service = OrganizationServiceImpl(
        repository,
    )

    response = service.get(
        organization.id,
    )

    assert response.id == organization.id