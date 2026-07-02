from uuid import uuid4

from backend.execution.projections.execution_projection import (
    ExecutionProjection,
)
from backend.execution.projections.execution_projection_store import (
    ExecutionProjectionStore,
)


def make_projection() -> ExecutionProjection:
    return ExecutionProjection(
        execution_id=uuid4(),
        trace_id=uuid4(),
    )


def test_save_and_get():
    store = ExecutionProjectionStore()

    projection = make_projection()

    store.save(projection)

    assert (
        store.get(projection.execution_id)
        is projection
    )


def test_get_unknown_returns_none():
    store = ExecutionProjectionStore()

    assert store.get(uuid4()) is None


def test_all():
    store = ExecutionProjectionStore()

    first = make_projection()
    second = make_projection()

    store.save(first)
    store.save(second)

    projections = store.all()

    assert len(projections) == 2
    assert first in projections
    assert second in projections


def test_clear():
    store = ExecutionProjectionStore()

    store.save(make_projection())

    store.clear()

    assert store.all() == []