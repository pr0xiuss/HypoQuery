from backend.optimization.history.repositories.execution_record_repository import (
    ExecutionRecordRepository,
)


def test_repository_is_abstract():

    try:

        ExecutionRecordRepository()

        assert False

    except TypeError:

        assert True