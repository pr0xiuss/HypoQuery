from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class WorkloadDTO(BaseModel):
    fingerprint_id: str
    query_text_snippet: str
    execution_count: int
    last_executed_at: Optional[datetime]

class ListWorkloadsResponse(BaseModel):
    workloads: List[WorkloadDTO]
    total_count: int
