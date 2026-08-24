from fastapi import APIRouter, Depends, Query
from backend.product.workloads.dtos import ListWorkloadsResponse
from backend.product.workloads.workload_service import WorkloadService
from backend.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/workloads", tags=["Workloads"])

from backend.api.dependencies.product import get_workload_service

@router.get("/", response_model=ListWorkloadsResponse)
def list_workloads(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: WorkloadService = Depends(get_workload_service),
    current_user = Depends(get_current_user)
) -> ListWorkloadsResponse:
    """
    Returns a product view of workloads based on execution data.
    """
    return service.list_workloads(limit=limit, offset=offset)
