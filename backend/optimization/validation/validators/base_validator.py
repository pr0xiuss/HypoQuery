from __future__ import annotations

from abc import ABC, abstractmethod

from backend.optimization.validation.context import (
    ValidationContext,
)
from backend.optimization.validation.models.validation_collection import (
    ValidationCollection,
)


class RecommendationValidator(ABC):
    """
    Base contract for all recommendation validators.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique validator name.
        """
        ...

    @property
    @abstractmethod
    def supported_keys(
        self,
    ) -> set[str]:
        """
        Recommendation codes supported by this validator.
        """
        ...

    @abstractmethod
    def validate(self, context: ValidationContext,) -> ValidationCollection:
        """
        Validates one or more recommendations.
        """
        ...