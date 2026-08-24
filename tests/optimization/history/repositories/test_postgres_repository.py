import pytest
from uuid import uuid4
from datetime import datetime, UTC
from backend.optimization.history.repositories.postgres_repository import (
    PostgresExecutionRecordRepository,
)
from backend.optimization.history.models.execution_record import ExecutionRecord
from backend.optimization.history.models.execution_metadata import ExecutionMetadata
from backend.optimization.history.models.execution_summary import ExecutionSummary
from backend.optimization.history.models.optimization_snapshot import OptimizationSnapshot
from backend.optimization.reporting.models.report_summary import ReportSummary
from backend.optimization.analysis.models.finding import Finding
from backend.optimization.history.search.search_criteria import SearchCriteria

def test_repository_creation(db_connection):
    repository = PostgresExecutionRecordRepository(db_connection)
    assert repository is not None

def test_save_and_find_record(db_connection):
    repository = PostgresExecutionRecordRepository(db_connection)
    execution_id = uuid4()
    trace_id = uuid4()
    
    metadata = ExecutionMetadata(
        execution_id=execution_id,
        trace_id=trace_id,
        fingerprint="SELECT 1",
        normalized_sql="SELECT ?",
        pipeline_name="test_pipeline",
        pipeline_version="1.0",
        database="test_db",
        schema="public",
        executed_at=datetime.now(UTC),
    )
    
    summary = ExecutionSummary(
        total_recommendations=5,
        validated_recommendations=2,
        total_strategies=1,
        estimated_improvement_percent=25.5,
        highest_strategy_score=90.0,
    )
    
    snapshot = OptimizationSnapshot(
        summary=ReportSummary(
            has_recommendations=True,
            total_recommendations=5,
            validated_recommendations=2,
            total_strategies=1,
            estimated_improvement_percent=25.5,
            highest_strategy_score=90.0,
        )
    )
    
    record = ExecutionRecord(
        metadata=metadata,
        summary=summary,
        snapshot=snapshot,
    )
    
    repository.save(record)
    
    retrieved = repository.find(execution_id)
    assert retrieved is not None
    assert retrieved.metadata.execution_id == execution_id
    assert retrieved.metadata.fingerprint == "SELECT 1"
    assert retrieved.summary.total_recommendations == 5

def test_list_and_search_records(db_connection):
    repository = PostgresExecutionRecordRepository(db_connection)
    execution_id = uuid4()
    
    metadata = ExecutionMetadata(
        execution_id=execution_id,
        trace_id=uuid4(),
        fingerprint="SELECT * FROM test",
        normalized_sql="SELECT * FROM ?",
        pipeline_name="test_pipeline",
        pipeline_version="1.0",
        database="test_db",
        schema="public",
        executed_at=datetime.now(UTC),
    )
    
    summary = ExecutionSummary(
        total_recommendations=0,
        validated_recommendations=0,
        total_strategies=0,
        estimated_improvement_percent=0.0,
        highest_strategy_score=0.0,
    )
    
    snapshot = OptimizationSnapshot(
        summary=ReportSummary(
            has_recommendations=False,
            total_recommendations=0,
            validated_recommendations=0,
            total_strategies=0,
            estimated_improvement_percent=0.0,
            highest_strategy_score=0.0,
        ),
    )
    
    record = ExecutionRecord(
        metadata=metadata,
        summary=summary,
        snapshot=snapshot,
    )
    
    repository.save(record)
    
    # test list
    records = repository.list()
    assert len(records) >= 1
    
    # test search
    criteria = SearchCriteria(fingerprint="SELECT * FROM test")
    search_result = repository.search(criteria)
    assert len(search_result.records) >= 1
    assert search_result.records[0].metadata.execution_id == execution_id