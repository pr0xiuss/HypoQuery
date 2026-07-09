from uuid import uuid4

from backend.optimization.history.models.execution_metadata import (
    ExecutionMetadata,
)
from backend.optimization.history.models.execution_record import (
    ExecutionRecord,
)
from backend.optimization.history.models.execution_summary import (
    ExecutionSummary,
)
from backend.optimization.history.models.optimization_snapshot import (
    OptimizationSnapshot,
)
from backend.optimization.history.repositories.memory_repository import (
    MemoryExecutionRecordRepository,
)
from backend.optimization.history.search.search_criteria import (
    SearchCriteria,
)
from backend.optimization.reporting.models.optimization_report import (
    OptimizationReport,
)
from backend.optimization.reporting.models.report_summary import (
    ReportSummary,
)


def create_record():

    metadata = ExecutionMetadata(
        execution_id=uuid4(),
        trace_id=uuid4(),
        fingerprint="fp",
        normalized_sql="SELECT 1;",
        pipeline_name="optimization",
        pipeline_version="1.0",
        database="postgres",
        schema="public",
    )

    return ExecutionRecord(
        metadata=metadata,
        summary=ExecutionSummary(
            total_recommendations=2,
            validated_recommendations=1,
            total_strategies=1,
            estimated_improvement_percent=80,
            highest_strategy_score=90,
        ),
        snapshot=OptimizationSnapshot(
            summary=ReportSummary(),
        ),
    )


def test_save_find_exists_count_delete():

    repository = MemoryExecutionRecordRepository()

    record = create_record()

    repository.save(
        record,
    )

    assert repository.exists(
        record.metadata.execution_id,
    )

    assert (
        repository.find(
            record.metadata.execution_id,
        )
        == record
    )

    assert repository.count() == 1

    repository.delete(
        record.metadata.execution_id,
    )

    assert repository.count() == 0


def test_search():

    repository = MemoryExecutionRecordRepository()

    record = create_record()

    repository.save(
        record,
    )

    result = repository.search(
        SearchCriteria(
            fingerprint="fp",
        )
    )

    assert result.total_records == 1

    assert result.records[0] == record