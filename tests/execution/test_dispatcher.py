from backend.execution.queue.memory_queue import InMemoryQueue
from backend.execution.workers.dispatcher import Dispatcher
from backend.execution.workers.worker import Worker

from tests.execution.test_pipeline_executor import build_executor


def make_worker():
    return Worker(
        queue=InMemoryQueue(),
        executor=build_executor(),
    )


def test_round_robin():
    workers = [
        make_worker(),
        make_worker(),
        make_worker(),
    ]

    dispatcher = Dispatcher(
        workers,
    )

    first = dispatcher.next_worker()
    second = dispatcher.next_worker()
    third = dispatcher.next_worker()
    fourth = dispatcher.next_worker()

    assert first is workers[0]
    assert second is workers[1]
    assert third is workers[2]
    assert fourth is workers[0]


def test_empty_dispatcher():
    dispatcher = Dispatcher([])

    assert dispatcher.next_worker() is None