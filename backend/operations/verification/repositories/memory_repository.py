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


class MemoryVerificationRepository(
    BaseVerificationRepository,
):
    """
    In-memory repository used for testing
    and local execution.
    """

    def __init__(self) -> None:
        self._verifications: dict[
            VerificationId,
            Verification,
        ] = {}

    def add(
        self,
        verification: Verification,
    ) -> None:
        self._verifications[
            verification.id
        ] = verification

    def find(
        self,
        verification_id: VerificationId,
    ) -> Verification | None:
        return self._verifications.get(
            verification_id,
        )

    def contains(
        self,
        verification_id: VerificationId,
    ) -> bool:
        return (
            verification_id
            in self._verifications
        )