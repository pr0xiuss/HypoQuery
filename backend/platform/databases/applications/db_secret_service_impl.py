from uuid import UUID
from uuid import uuid4

from backend.platform.databases.applications.db_secret_service import (
    DatabaseSecretService,
)


class DatabaseSecretServiceImpl(
    DatabaseSecretService,
):
    """
    Temporary implementation.

    Phase 7 stores secrets in-memory until the
    dedicated secrets subsystem is introduced.
    """

    def __init__(
        self,
    ) -> None:
        self._secrets: dict[UUID, str] = {}

    def create(
        self,
        password: str,
    ) -> UUID:
        secret_id = uuid4()

        self._secrets[
            secret_id
        ] = password

        return secret_id

    def get(
        self,
        secret_id: UUID,
    ) -> str:
        return self._secrets[
            secret_id
        ]

    def delete(
        self,
        secret_id: UUID,
    ) -> None:
        self._secrets.pop(
            secret_id,
            None,
        )