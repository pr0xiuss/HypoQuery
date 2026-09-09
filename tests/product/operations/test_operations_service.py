import pytest
import uuid
from datetime import datetime, UTC
from unittest.mock import MagicMock, call

from backend.observability.persistence.event_repository import EventRepository
from backend.observability.persistence.event_serializer import EventSerializer
from backend.product.operations.operations_service import OperationsService
from backend.execution.projections.execution_projection_store import ExecutionProjectionStore
from backend.execution.contracts.events.pipeline import (
    PipelineStartedEvent,
    PipelineCompletedEvent,
    PipelineFailedEvent,
)
from backend.execution.events.metadata import EventMetadata
from backend.execution.contracts.events.enums import EventVersion

@pytest.fixture
def mock_connection():
    conn = MagicMock()
    conn.cursor.return_value.__enter__.return_value = MagicMock()
    return conn

@pytest.fixture
def event_repository(mock_connection):
    return EventRepository(connection=mock_connection, serializer=EventSerializer())

@pytest.fixture
def operations_service(event_repository):
    store = ExecutionProjectionStore()
    return OperationsService(
        execution_projection_store=store,
        event_repository=event_repository
    )

def _create_event(event_cls, execution_id, **kwargs):
    metadata = EventMetadata(
        event_id=uuid.uuid4(),
        execution_id=execution_id,
        trace_id=uuid.uuid4(),
        sequence_number=1,
        timestamp=datetime.now(UTC),
        event_version=EventVersion.V1
    )
    return event_cls(metadata=metadata, **kwargs)

def test_event_persistence(event_repository, mock_connection):
    exec_id = uuid.uuid4()
    event = _create_event(PipelineStartedEvent, exec_id)
    
    event_repository.save(event)
    
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    assert cursor_mock.execute.called
    args = cursor_mock.execute.call_args[0]
    assert "INSERT INTO execution_events" in args[0]
    assert args[1][1] == str(exec_id)
    assert args[1][3] == "PipelineStartedEvent"
    assert mock_connection.commit.called

def test_empty_execution_events(operations_service, mock_connection):
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = []
    
    res = operations_service.list_operations()
    assert len(res.operations) == 0
    assert res.total_count == 0

def test_completed_execution(operations_service, mock_connection):
    exec_id = uuid.uuid4()
    now = datetime.now(UTC)
    
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    # First query returns distinct execution_ids
    # Second query returns events
    cursor_mock.fetchall.side_effect = [
        [(str(exec_id),)],
        [
            (uuid.uuid4(), str(exec_id), uuid.uuid4(), "PipelineStartedEvent", 1, now, {}),
            (uuid.uuid4(), str(exec_id), uuid.uuid4(), "PipelineCompletedEvent", 1, now, {"duration_ms": 100})
        ]
    ]
    
    res = operations_service.list_operations()
    assert len(res.operations) == 1
    op = res.operations[0]
    assert op.operation_id == str(exec_id)
    assert op.status == "COMPLETED"

def test_failed_execution(operations_service, mock_connection):
    exec_id = uuid.uuid4()
    now = datetime.now(UTC)
    
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.side_effect = [
        [(str(exec_id),)],
        [
            (uuid.uuid4(), str(exec_id), uuid.uuid4(), "PipelineStartedEvent", 1, now, {}),
            (uuid.uuid4(), str(exec_id), uuid.uuid4(), "PipelineFailedEvent", 1, now, {"error": "DB Error"})
        ]
    ]
    
    res = operations_service.list_operations()
    assert len(res.operations) == 1
    op = res.operations[0]
    assert op.operation_id == str(exec_id)
    assert op.status == "FAILED"

def test_multiple_executions_and_pagination(event_repository, mock_connection):
    exec_1 = uuid.uuid4()
    exec_2 = uuid.uuid4()
    now = datetime.now(UTC)
    
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.side_effect = [
        [(str(exec_1),), (str(exec_2),)],
        [
            (uuid.uuid4(), str(exec_1), uuid.uuid4(), "PipelineStartedEvent", 1, now, {}),
            (uuid.uuid4(), str(exec_2), uuid.uuid4(), "PipelineStartedEvent", 1, now, {})
        ]
    ]
    
    events = event_repository.list_executions(limit=2, offset=0)
    assert len(events) == 2
    
    execute_calls = cursor_mock.execute.call_args_list
    assert "LIMIT %s OFFSET %s" in execute_calls[0][0][0]
    assert execute_calls[0][0][1] == (2, 0)

def test_get_execution(operations_service, mock_connection):
    exec_id = uuid.uuid4()
    now = datetime.now(UTC)
    
    cursor_mock = mock_connection.cursor.return_value.__enter__.return_value
    cursor_mock.fetchall.return_value = [
        (uuid.uuid4(), str(exec_id), uuid.uuid4(), "PipelineStartedEvent", 1, now, {}),
        (uuid.uuid4(), str(exec_id), uuid.uuid4(), "PipelineFailedEvent", 1, now, {"error": "Syntax Error"})
    ]
    
    detail = operations_service.get_operation_detail(str(exec_id))
    assert detail.operation_id == str(exec_id)
    assert detail.status == "FAILED"
    assert detail.error_message == "Syntax Error"
