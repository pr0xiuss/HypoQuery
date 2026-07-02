from backend.execution.queue.memory_queue import InMemoryQueue
from backend.execution.workers.worker import Worker
from backend.execution.workers.worker_pool import WorkerPool

from tests.execution.test_pipeline_executor import build_executor


def make_worker():
    return Worker(
        queue=InMemoryQueue(),
        executor=build_executor(),
    )


def test_add_worker():
    pool = WorkerPool()

    pool.add_worker(
        make_worker(),
    )

    assert pool.size() == 1


def test_all_workers():
    pool = WorkerPool()

    pool.add_worker(make_worker())
    pool.add_worker(make_worker())

    workers = pool.all()

    assert len(workers) == 2


def test_returns_copy():
    pool = WorkerPool()

    pool.add_worker(
        make_worker(),
    )

    workers = pool.all()

    workers.clear()

    assert pool.size() == 1