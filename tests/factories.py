from datetime import UTC
from datetime import datetime
from uuid import uuid4

from backend.platform.auth.domain.user import User
from backend.platform.environments.domain.environment import (
    Environment,
)
from backend.platform.organizations.domain.organization import (
    Organization,
)
from backend.platform.projects.domain.project import Project


def create_user(**kwargs) -> User:
    now = datetime.now(UTC)

    defaults = {
        "id": uuid4(),
        "username": "john",
        "email": "john@example.com",
        "password_hash": "hashed-password",
        "is_active": True,
        "is_verified": True,
        "created_at": now,
        "updated_at": now,
    }

    defaults.update(kwargs)

    return User(**defaults)


def create_organization(**kwargs) -> Organization:
    now = datetime.now(UTC)

    unique = uuid4().hex[:8]

    defaults = {
        "id": uuid4(),
        "name": f"Acme-{unique}",
        "slug": f"acme-{unique}",
        "description": "Test Org",
        "created_at": now,
        "updated_at": now,
    }

    defaults.update(kwargs)

    return Organization(**defaults)


def create_project(
    organization_id,
    **kwargs,
) -> Project:
    now = datetime.now(UTC)

    defaults = {
        "id": uuid4(),
        "organization_id": organization_id,
        "name": "Platform",
        "slug": "platform",
        "description": "Test project",
        "created_at": now,
        "updated_at": now,
    }

    defaults.update(kwargs)

    return Project(**defaults)


def create_environment(
    project_id,
    **kwargs,
) -> Environment:
    now = datetime.now(UTC)

    defaults = {
        "id": uuid4(),
        "project_id": project_id,
        "name": "Development",
        "slug": "development",
        "description": "Development environment",
        "created_at": now,
        "updated_at": now,
    }

    defaults.update(kwargs)

    return Environment(**defaults)