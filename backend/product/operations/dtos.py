from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OperationSummaryDTO(BaseModel):
    operation_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    type: str

class OperationDetailDTO(BaseModel):
    operation_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    type: str
    logs_url: Optional[str]
    error_message: Optional[str]

class ListOperationsResponse(BaseModel):
    operations: List[OperationSummaryDTO]
    total_count: int
