from backend.product.dashboard.dtos import DashboardResponse, DashboardStatsDTO
from backend.execution.projections.execution_projection_store import ExecutionProjectionStore
from backend.optimization.history.repositories.execution_record_repository import ExecutionRecordRepository

class DashboardService:
    """
    Thin aggregation layer for dashboard metrics.
    """
    def __init__(
        self,
        execution_projection_store: ExecutionProjectionStore,
        execution_record_repository: ExecutionRecordRepository
    ):
        self.execution_projection_store = execution_projection_store
        self.execution_record_repository = execution_record_repository

    def get_dashboard_summary(self) -> DashboardResponse:
        active_queries = len(self.execution_projection_store.all())
        records = self.execution_record_repository.list()
        
        fingerprints = set(r.metadata.fingerprint for r in records)
        total_workloads = len(fingerprints)
        
        optimizations_applied = sum(len(r.snapshot.recommendations) for r in records)
        
        stats = DashboardStatsDTO(
            total_workloads=total_workloads,
            active_queries=active_queries,
            optimizations_applied=optimizations_applied
        )
        return DashboardResponse(stats=stats)
