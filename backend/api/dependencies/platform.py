from fastapi import Request
from fastapi import Depends
from backend.platform.bootstrap.container import PlatformContainer
from dependency_injector.wiring import Provide
from backend.platform.auth.application.authentication_service import AuthenticationService
from backend.platform.bootstrap.container import PlatformContainer
from backend.platform.organizations.application.organization_service import OrganizationService
from backend.platform.environments.application.environment_service import EnvironmentService
from backend.platform.projects.application.project_service import ProjectService
from backend.api.dependencies.container import get_container



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


