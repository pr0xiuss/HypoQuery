from __future__ import annotations

from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.verification.models.verification import (
    Verification,
)
from backend.operations.verification.repositories.base_repository import (
    BaseVerificationRepository,
)


class VerificationEngine:
    """
    Domain engine responsible for
    Verification operations.
    """

    def __init__(
        self,
        repository: BaseVerificationRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        verification: Verification,
    ) -> None:
        self._repository.add(
            verification,
        )

    def find(
        self,
        verification_id: VerificationId,
    ) -> Verification | None:
        return self._repository.find(
            verification_id,
        )

    def contains(
        self,
        verification_id: VerificationId,
    ) -> bool:
        return self._repository.contains(
            verification_id,
        )