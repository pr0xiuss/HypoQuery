from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuerySummaryDTO(BaseModel):
    query_id: str
    fingerprint_id: str
    query_text: str
    execution_time_ms: float
    timestamp: datetime

class QueryDetailDTO(BaseModel):
    query_id: str
    fingerprint_id: str
    query_text: str
    execution_time_ms: float
    timestamp: datetime
    # We compose findings and validations, but we don't dump the entire snapshot.
    has_optimizations: bool
    optimization_snapshot_id: Optional[str]
    total_recommendations: int

class ListQueriesResponse(BaseModel):
    queries: List[QuerySummaryDTO]
    total_count: int
