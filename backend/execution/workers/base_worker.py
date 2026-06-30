from __future__ import annotations

from abc import ABC, abstractmethod

from backend.execution.contracts.result import PipelineResult


class BaseWorker(ABC):
    """
    Base contract for all worker implementations.
    """

    @abstractmethod
    def process(self) -> PipelineResult | None:
        """
        Process a single queue entry.

        Returns:
            PipelineResult if work was processed.
            None if no work was available.
        """
        raise NotImplementedError