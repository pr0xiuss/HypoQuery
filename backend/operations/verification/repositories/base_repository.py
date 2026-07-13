from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.operations.models.identifiers import (
    VerificationId,
)
from backend.operations.verification.models.verification import (
    Verification,
)


class BaseVerificationRepository(ABC):
    """
    Repository contract for Verification aggregates.
    """

    @abstractmethod
    def add(
        self,
        verification: Verification,
    ) -> None:
        """
        Add a Verification.
        """

    @abstractmethod
    def find(
        self,
        verification_id: VerificationId,
    ) -> Verification | None:
        """
        Find a Verification.
        """

    @abstractmethod
    def contains(
        self,
        verification_id: VerificationId,
    ) -> bool:
        """
        Determine whether a Verification exists.
        """