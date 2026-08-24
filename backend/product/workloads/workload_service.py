from backend.product.workloads.dtos import ListWorkloadsResponse, WorkloadDTO
from backend.optimization.history.repositories.execution_record_repository import ExecutionRecordRepository
from collections import defaultdict

class WorkloadService:
    """
    Service to project ExecutionRecords and QueryFingerprints 
    into a product-facing Workload view.
    """
    def __init__(self, execution_record_repository: ExecutionRecordRepository):
        self.execution_record_repository = execution_record_repository

    def list_workloads(self, limit: int = 100, offset: int = 0) -> ListWorkloadsResponse:
        records = self.execution_record_repository.list()
        
        # Group by fingerprint
        workloads = defaultdict(list)
        for r in records:
            workloads[r.metadata.fingerprint].append(r)
            
        dtos = []
        for fingerprint, recs in workloads.items():
            # sort by executed_at desc
            recs.sort(key=lambda x: x.metadata.executed_at, reverse=True)
            last_executed = recs[0]
            
            dtos.append(
                WorkloadDTO(
                    fingerprint_id=fingerprint,
                    query_text_snippet=last_executed.metadata.normalized_sql[:100],
                    execution_count=len(recs),
                    last_executed_at=last_executed.metadata.executed_at
                )
            )
            
        dtos.sort(key=lambda x: x.last_executed_at, reverse=True)
        
        return ListWorkloadsResponse(
            workloads=dtos[offset:offset+limit],
            total_count=len(dtos)
        )
