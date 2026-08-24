from fastapi import APIRouter, Depends
from backend.product.dashboard.dtos import DashboardResponse
from backend.product.dashboard.dashboard_service import DashboardService
from backend.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

from backend.api.dependencies.product import get_dashboard_service

@router.get("/", response_model=DashboardResponse)
def get_dashboard(
    service: DashboardService = Depends(get_dashboard_service),
    current_user = Depends(get_current_user)
) -> DashboardResponse:
    """
    Returns the aggregated dashboard view.
    """
    return service.get_dashboard_summary()
