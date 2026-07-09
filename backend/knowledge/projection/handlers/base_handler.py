from __future__ import annotations

from abc import ABC, abstractmethod
from backend.knowledge.projection.models.projection_result import ProjectionResult
from backend.knowledge.projection.context import ProjectionContext


class Projector(ABC):
    """
    Base contract for every Knowledge Projection domain.

    A Projector transforms deterministic optimization
    artifacts into reusable optimization knowledge.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique projector name."""
        raise NotImplementedError

    @abstractmethod
    def project(
        self,
        context: ProjectionContext,
    ) -> ProjectionResult:
        """
        Project optimization knowledge.

        Returns immutable knowledge artifacts that will
        later be merged into the KnowledgeGraph.
        """
        raise NotImplementedError