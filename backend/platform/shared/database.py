from collections.abc import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from backend.platform.config.settings import get_settings

settings = get_settings()

DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.database_user}:"
    f"{settings.database_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_name}"
)

engine = create_engine(
    DATABASE_URL,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """
    Base class for all platform ORM models.
    """


def get_db_session() -> Generator[Session, None, None]:
    """
    Create a SQLAlchemy session.
    """

    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def verify_database_connection() -> None:
    """
    Verifies that the platform database is reachable.
    """

    with engine.connect() as connection:
        connection.execute(
            text("SELECT 1"),
        )


def import_models() -> None:
    """
    Imports all ORM models so they are registered
    with SQLAlchemy metadata.
    """

    from backend.platform.auth.infra.user_model import (
        UserModel,
    )
    from backend.platform.environments.infra.environment_model import (
        EnvironmentModel,
    )
    from backend.platform.organizations.infra.organization_model import (
        OrganizationModel,
    )
    from backend.platform.projects.infra.project_model import (
        ProjectModel,
    )
    from backend.platform.databases.infra.db_connection_model import (
        DatabaseConnectionModel,
    )
    from backend.platform.databases.infra.db_metadata_model import (
        DatabaseMetadataModel,
    )
    from backend.platform.apis.infra.api_model import (
        ApiModel
    )
    from backend.platform.access_control.infra.org_membership_model import (
        OrganizationMembershipModel,
    )
    from backend.platform.apis.infra.api_endpoint_model import (
        ApiEndpointModel,
    )
    from backend.platform.scheduler.infra.job_model import (
        JobModel,
    )
    from backend.platform.scheduler.infra.schedule_model import (
        ScheduleModel,
    )
    from backend.platform.notifications.infra.notification_model import (
        NotificationModel,
    )
    from backend.platform.notifications.infra.preference_model import (
        NotificationPreferenceModel,
    )
    _ = (
        UserModel,
        OrganizationModel,
        ProjectModel,
        EnvironmentModel,
        DatabaseConnectionModel,
        DatabaseMetadataModel,
        ApiModel,
        OrganizationMembershipModel,
        ApiEndpointModel,
        JobModel,
        ScheduleModel,
        NotificationModel,
        NotificationPreferenceModel,
    )