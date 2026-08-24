from backend.product.operations.dtos import ListOperationsResponse, OperationDetailDTO, OperationSummaryDTO
from backend.execution.projections.execution_projection_store import ExecutionProjectionStore
from backend.observability.persistence.event_repository import EventRepository
from datetime import datetime, UTC
from typing import Optional
import uuid

class OperationsService:
    """
    Read-only service projecting ExecutionProjectionStore (running) 
    and EventRepository (historical) into a unified Operations view.
    """
    def __init__(
        self,
        execution_projection_store: ExecutionProjectionStore,
        event_repository: EventRepository,
    ):
        self.execution_projection_store = execution_projection_store
        self.event_repository = event_repository

    def list_operations(self, limit: int = 100, offset: int = 0) -> ListOperationsResponse:
        operations = []
        
        # 1. Fetch active operations from projection store
        projections = self.execution_projection_store.all()
        active_ids = set()
        for p in projections:
            active_ids.add(str(p.execution_id))
            operations.append(
                OperationSummaryDTO(
                    operation_id=str(p.execution_id),
                    status=p.status.value if hasattr(p.status, 'value') else str(p.status),
                    created_at=p.started_at or datetime.now(UTC),
                    updated_at=p.completed_at or datetime.now(UTC),
                    type="PIPELINE_EXECUTION"
                )
            )
            
        # 2. Fetch historical operations from event repository
        events = self.event_repository.list_executions(limit=limit, offset=offset)
        
        # Group events by execution_id
        executions = {}
        for ev in events:
            eid = ev["execution_id"]
            if eid not in executions:
                executions[eid] = []
            executions[eid].append(ev)

        for eid, ev_list in executions.items():
            if eid in active_ids:
                continue
                
            status_str = "RUNNING"
            start_time = None
            end_time = None
            error_msg = None
            
            for ev in ev_list:
                if ev["event_type"] == "PipelineStartedEvent":
                    start_time = ev["occurred_at"]
                elif ev["event_type"] == "PipelineCompletedEvent":
                    status_str = "COMPLETED"
                    end_time = ev["occurred_at"]
                elif ev["event_type"] == "PipelineFailedEvent":
                    status_str = "FAILED"
                    end_time = ev["occurred_at"]
                    error_msg = ev["payload"].get("error", "Unknown error")
                    
            if not start_time and ev_list:
                start_time = ev_list[0]["occurred_at"]
            if not end_time and ev_list:
                end_time = ev_list[-1]["occurred_at"]
                
            operations.append(
                OperationSummaryDTO(
                    operation_id=eid,
                    status=status_str,
                    created_at=start_time or datetime.now(UTC),
                    updated_at=end_time or datetime.now(UTC),
                    type="PIPELINE_EXECUTION"
                )
            )

        return ListOperationsResponse(
            operations=operations[:limit],
            total_count=len(operations)
        )

    def get_operation_detail(self, operation_id: str) -> OperationDetailDTO:
        # Check if active (projection)
        try:
            uid = uuid.UUID(operation_id)
            p = self.execution_projection_store.get(uid)
            if p:
                return OperationDetailDTO(
                    operation_id=str(p.execution_id),
                    status=p.status.value if hasattr(p.status, 'value') else str(p.status),
                    created_at=p.started_at or datetime.now(UTC),
                    updated_at=p.completed_at or datetime.now(UTC),
                    type="PIPELINE_EXECUTION",
                    logs_url=None,
                    error_message=None
                )
        except ValueError:
            pass

        # Check historical
        ev_list = self.event_repository.get_execution(operation_id)
        if ev_list:
            status_str = "RUNNING"
            start_time = None
            end_time = None
            error_msg = None
            
            for ev in ev_list:
                if ev["event_type"] == "PipelineStartedEvent":
                    start_time = ev["occurred_at"]
                elif ev["event_type"] == "PipelineCompletedEvent":
                    status_str = "COMPLETED"
                    end_time = ev["occurred_at"]
                elif ev["event_type"] == "PipelineFailedEvent":
                    status_str = "FAILED"
                    end_time = ev["occurred_at"]
                    error_msg = ev["payload"].get("error", "Unknown error")
                    
            if not start_time and ev_list:
                start_time = ev_list[0]["occurred_at"]
            if not end_time and ev_list:
                end_time = ev_list[-1]["occurred_at"]
                
            return OperationDetailDTO(
                operation_id=operation_id,
                status=status_str,
                created_at=start_time or datetime.now(UTC),
                updated_at=end_time or datetime.now(UTC),
                type="PIPELINE_EXECUTION",
                logs_url=None,
                error_message=error_msg
            )
        
        raise ValueError(f"Operation {operation_id} not found")
