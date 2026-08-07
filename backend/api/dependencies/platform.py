from fastapi import Request
from backend.platform.apis.discovery.application.discovery_service import DiscoveryService
from backend.platform.auth.application.authentication_service import AuthenticationService
from backend.platform.organizations.application.organization_service import OrganizationService
from backend.platform.environments.application.environment_service import EnvironmentService
from backend.platform.projects.application.project_service import ProjectService
from backend.api.dependencies.container import get_container
from backend.platform.apis.discovery.application.discovery_service import DiscoveryService


def get_authentication_service(
    request: Request,
) -> AuthenticationService:
    """
    Returns the authentication application service.
    """

    container = get_container(request)

    return container.authentication_service()


def get_organization_service(
    request: Request,
) -> OrganizationService:
    """
    Returns the organization application service.
    """

    container = get_container(request)

    return container.organization_service()


def get_project_service(
    request: Request,
) -> ProjectService:
    """
    Returns the project application service.
    """

    container = get_container(request)

    return container.project_service()


def get_environment_service(
    request: Request,
) -> EnvironmentService:
    """
    Returns the environment application service.
    """

    container = get_container(request)

    return container.environment_service()


def get_discovery_service(
    request: Request,
) -> DiscoveryService:
    """
    Returns the API discovery orchestrator.
    """

    container = get_container(
        request,
    )

    return container.discovery_service()