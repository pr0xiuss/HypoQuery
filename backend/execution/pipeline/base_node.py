from __future__ import annotations

from abc import ABC, abstractmethod

from backend.execution.contracts.execution import PipelineExecution
from backend.execution.contracts.node_result import NodeResult


class PipelineNode(ABC):
    """
    Base contract for every pipeline node.

    A node performs exactly one responsibility and enriches the PipelineState.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique node name within a pipeline."""
        raise NotImplementedError

    def can_execute(self, execution: PipelineExecution) -> bool:
        """Whether this node should execute."""
        return True

    def before_execute(self, execution: PipelineExecution) -> None:
        """Hook executed before execute()."""
        pass

    @abstractmethod
    def execute(self, execution: PipelineExecution) -> NodeResult:
        """Business logic."""
        raise NotImplementedError

    def after_execute(
        self,
        execution: PipelineExecution,
        result: NodeResult,
    ) -> None:
        """Hook executed after execute()."""
        pass

    def on_error(
        self,
        execution: PipelineExecution,
        exception: Exception,
    ) -> None:
        """Hook executed when execute() raises."""
        pass

    def cleanup(self, execution: PipelineExecution) -> None:
        """Always executed before leaving the node."""
        pass

