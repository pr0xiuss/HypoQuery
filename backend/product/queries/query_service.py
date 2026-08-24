from backend.product.queries.dtos import ListQueriesResponse, QueryDetailDTO, QuerySummaryDTO
from backend.optimization.history.repositories.execution_record_repository import ExecutionRecordRepository
from backend.optimization.history.search.search_criteria import SearchCriteria
from typing import Optional
import uuid

class QueryService:
    """
    Thin product query layer over execution, history, optimization snapshot, 
    recommendation, and validation contracts.
    """
    def __init__(self, execution_record_repository: ExecutionRecordRepository):
        self.execution_record_repository = execution_record_repository

    def list_queries(self, fingerprint_id: Optional[str] = None, limit: int = 100, offset: int = 0) -> ListQueriesResponse:
        if fingerprint_id:
            criteria = SearchCriteria(fingerprint=fingerprint_id)
            result = self.execution_record_repository.search(criteria)
            records = result.records
        else:
            records = self.execution_record_repository.list()
            
        records = sorted(records, key=lambda r: r.metadata.executed_at, reverse=True)
        
        queries = []
        for r in records[offset:offset+limit]:
            queries.append(
                QuerySummaryDTO(
                    query_id=str(r.metadata.execution_id),
                    fingerprint_id=r.metadata.fingerprint,
                    query_text=r.metadata.normalized_sql,
                    execution_time_ms=0,
                    timestamp=r.metadata.executed_at
                )
            )
            
        return ListQueriesResponse(
            queries=queries,
            total_count=len(records)
        )

    def get_query_detail(self, query_id: str) -> QueryDetailDTO:
        try:
            uid = uuid.UUID(query_id)
        except ValueError:
            raise ValueError(f"Invalid query_id format: {query_id}")
            
        record = self.execution_record_repository.find(uid)
        if not record:
            raise ValueError(f"Query {query_id} not found")
            
        return QueryDetailDTO(
            query_id=str(record.metadata.execution_id),
            fingerprint_id=record.metadata.fingerprint,
            query_text=record.metadata.normalized_sql,
            execution_time_ms=0,
            timestamp=record.metadata.executed_at,
            has_optimizations=len(record.snapshot.recommendations) > 0,
            optimization_snapshot_id=str(record.metadata.execution_id),
            total_recommendations=len(record.snapshot.recommendations)
        )
