import pytest
from fastapi import Request
from backend.api.main import app
from backend.platform.bootstrap.container import PlatformContainer

def test_module_5_di_resolution():
    container = PlatformContainer()
    
    # Verify we can resolve the services
    dashboard_service = container.dashboard_service()
    assert dashboard_service is not None
    
    workload_service = container.workload_service()
    assert workload_service is not None
    
    query_service = container.query_service()
    assert query_service is not None
    
    # We cannot resolve operations_service without injecting a mocked connection
    # because psycopg_connection tries to connect immediately when Factory is called if not mocked,
    # or actually it's a provider, so it doesn't connect until used.
    # Let's mock the psycopg connection factory
    from unittest.mock import MagicMock
    mock_conn = MagicMock()
    
    with container.psycopg_connection.override(mock_conn):
        operations_service = container.operations_service()
        assert operations_service is not None
        assert operations_service.event_repository is not None
        assert operations_service.execution_projection_store is not None

    # Test Assistant and Knowledge facades
    assistant_facade = container.assistant_service_facade()
    assert assistant_facade is not None

    context_service = container.context_service()
    assert context_service is not None

    explanation_service = container.explanation_service()
    assert explanation_service is not None

