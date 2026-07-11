from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from backend.knowledge.models.explanation_snapshot import (
    ExplanationSnapshot,
)


class AudienceProfile(ABC):
    """
    Defines how an explanation should be
    adapted for a specific audience.
    """

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Unique profile name.
        """

    @abstractmethod
    def transform(
        self,
        explanation: ExplanationSnapshot,
    ) -> ExplanationSnapshot:
        """
        Adapt an explanation for the target
        audience.
        """