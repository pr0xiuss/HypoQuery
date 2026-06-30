from backend.execution.contracts.job import PipelineJob
from backend.execution.queue.job_record import QueueEntry
from backend.execution.queue.memory_queue import InMemoryQueue


def make_entry(source: str) -> QueueEntry:
    return QueueEntry(
        job=PipelineJob(
            source=source,
            pipeline_version="1.0",
        )
    )


def test_new_queue_is_empty():

    queue = InMemoryQueue()

    assert queue.is_empty()
    assert queue.size() == 0
    assert queue.peek() is None
    assert queue.dequeue() is None


def test_enqueue():

    queue = InMemoryQueue()

    queue.enqueue(make_entry("job1"))

    assert not queue.is_empty()
    assert queue.size() == 1


def test_peek():

    queue = InMemoryQueue()

    entry = make_entry("job1")

    queue.enqueue(entry)

    assert queue.peek() == entry
    assert queue.size() == 1


def test_dequeue():

    queue = InMemoryQueue()

    entry = make_entry("job1")

    queue.enqueue(entry)

    removed = queue.dequeue()

    assert removed == entry
    assert queue.is_empty()


def test_fifo_order():

    queue = InMemoryQueue()

    first = make_entry("first")
    second = make_entry("second")
    third = make_entry("third")

    queue.enqueue(first)
    queue.enqueue(second)
    queue.enqueue(third)

    assert queue.dequeue() == first
    assert queue.dequeue() == second
    assert queue.dequeue() == third

    assert queue.is_empty()


def test_size_updates():

    queue = InMemoryQueue()

    queue.enqueue(make_entry("a"))
    queue.enqueue(make_entry("b"))

    assert queue.size() == 2

    queue.dequeue()

    assert queue.size() == 1

    queue.dequeue()

    assert queue.size() == 0