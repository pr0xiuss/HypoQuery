from abc import ABC, abstractmethod

from backend.execution.contracts.execution import PipelineExecution


class Lifecycle(ABC):

    @abstractmethod
    def queue(self, execution: PipelineExecution,) -> None:
        ...

    @abstractmethod
    def assign(self, execution: PipelineExecution,) -> None:
        ...

    @abstractmethod
    def start(self, execution: PipelineExecution,) -> None:
        ...

    @abstractmethod
    def complete(self, execution: PipelineExecution,) -> None:
        ...

    @abstractmethod
    def fail(self, execution: PipelineExecution,) -> None:
        ...

    @abstractmethod
    def cancel(self, execution: PipelineExecution,) -> None:
        ...