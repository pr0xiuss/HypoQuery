from dataclasses import dataclass

from backend.execution.contracts.lifecycle import Lifecycle
from backend.execution.contracts.publisher import Publisher
from backend.execution.events.execution_event_factory import (
    ExecutionEventFactory,
)
from backend.execution.runtime.clock import Clock


@dataclass(frozen=True, slots=True)
class RuntimeContext:
    lifecycle: Lifecycle
    event_factory: ExecutionEventFactory
    publisher: Publisher
    clock: Clock