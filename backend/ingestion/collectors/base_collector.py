from __future__ import annotations

from abc import ABC, abstractmethod

from backend.execution.contracts.execution import PipelineExecution


class BaseCollector(ABC):
    """
    Base contract for all ingestion collectors.

    A collector is responsible for producing units of work
    (PipelineExecution objects). It does not enqueue or execute them.
    """

    @abstractmethod
    def collect(self) -> list[PipelineExecution]:
        """
        Collect work from a source.

        Returns:
            A list of PipelineExecution objects ready to be queued.
        """
        raise NotImplementedError