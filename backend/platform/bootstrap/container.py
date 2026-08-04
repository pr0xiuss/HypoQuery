from dependency_injector import containers
from dependency_injector import providers

from sqlalchemy.orm import Session

from backend.platform.auth.application.authentication_service import AuthenticationService
from backend.platform.auth.application.auth_service_impl import AuthenticationServiceImpl
from backend.platform.auth.infra.user_repository_imp import UserRepositoryImpl
from backend.platform.auth.repositories.user_repository import UserRepository
from backend.platform.config.settings import get_settings
from backend.platform.environments.application.environment_service import EnvironmentService
from backend.platform.environments.application.environment_service_impl import EnvironmentServiceImpl
from backend.platform.environments.infra.environment_repository_impl import EnvironmentRepositoryImpl
from backend.platform.environments.repositories.environment_repository import EnvironmentRepository
from backend.platform.organizations.application.organization_service import OrganizationService
from backend.platform.organizations.application.org_service_imp import OrganizationServiceImpl
from backend.platform.organizations.infra.org_repository_impl import OrganizationRepositoryImpl
from backend.platform.organizations.repositories.organization_repository import OrganizationRepository
from backend.platform.projects.application.project_service import ProjectService
from backend.platform.projects.application.project_service_impl import ProjectServiceImpl
from backend.platform.projects.infra.project_repository_impl import ProjectRepositoryImpl
from backend.platform.projects.repositories.project_repository import ProjectRepository
from backend.platform.shared.database import SessionLocal
from backend.platform.auth.application.password_hasher import PasswordHasher
from backend.platform.auth.infra.password_hasher_impl import PasswordHasherImpl
from backend.platform.auth.application.jwt_service import JWTService
from backend.platform.auth.infra.jwt_service_impl import JWTServiceImpl
from backend.platform.auth.application.jwt_service import JWTService
from backend.platform.auth.infra.jwt_service_impl import JWTServiceImpl
from backend.platform.auth.application.current_user_service import CurrentUserService
from backend.platform.auth.application.current_user_service_impl import CurrentUserServiceImpl


class PlatformContainer(containers.DeclarativeContainer):
    """
    Dependency Injection container for the Product Platform.
    """

    wiring_config = containers.WiringConfiguration(
        packages=[
            "backend.api",
        ]
    )

    settings = providers.Singleton(
        get_settings,
    )

    db_session: providers.Provider[Session] = providers.Factory(
        SessionLocal,
    )

    user_repository: providers.Provider[UserRepository] = providers.Factory(
        UserRepositoryImpl,
        session=db_session,
    )

    organization_repository: providers.Provider[
        OrganizationRepository
    ] = providers.Factory(
        OrganizationRepositoryImpl,
        session=db_session,
    )

    project_repository: providers.Provider[
        ProjectRepository
    ] = providers.Factory(
        ProjectRepositoryImpl,
        session=db_session,
    )

    environment_repository: providers.Provider[
        EnvironmentRepository
    ] = providers.Factory(
        EnvironmentRepositoryImpl,
        session=db_session,
    )

    password_hasher: providers.Provider[
        PasswordHasher
    ] = providers.Singleton(
        PasswordHasherImpl,
    )

    jwt_service: providers.Provider[
        JWTService
    ] = providers.Singleton(
        JWTServiceImpl,
        secret_key=settings.provided.jwt_secret,
        algorithm=settings.provided.jwt_algorithm,
        expires_in_minutes=settings.provided.jwt_expiration_minutes,
    )

    authentication_service: providers.Provider[
        AuthenticationService
    ] = providers.Factory(
        AuthenticationServiceImpl,
        user_repository=user_repository,
        password_hasher=password_hasher,
        jwt_service=jwt_service,
    )

    organization_service: providers.Provider[
        OrganizationService
    ] = providers.Factory(
        OrganizationServiceImpl,
        organization_repository=organization_repository,
    )

    project_service: providers.Provider[
        ProjectService
    ] = providers.Factory(
        ProjectServiceImpl,
        project_repository=project_repository,
    )

    environment_service: providers.Provider[
        EnvironmentService
    ] = providers.Factory(
        EnvironmentServiceImpl,
        environment_repository=environment_repository,
    )

    current_user_service: providers.Provider[
        CurrentUserService
    ] = providers.Factory(
        CurrentUserServiceImpl,
        user_repository=user_repository,
    )