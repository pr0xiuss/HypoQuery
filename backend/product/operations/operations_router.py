from fastapi import APIRouter, Depends, Query, Path
from backend.product.operations.dtos import ListOperationsResponse, OperationDetailDTO
from backend.product.operations.operations_service import OperationsService
from backend.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/operations", tags=["Operations"])

from backend.api.dependencies.product import get_operations_service

@router.get("/", response_model=ListOperationsResponse)
def list_operations(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: OperationsService = Depends(get_operations_service),
    current_user = Depends(get_current_user)
) -> ListOperationsResponse:
    """
    Returns a read-only list of operations from running and historical states.
    """
    return service.list_operations(limit=limit, offset=offset)

@router.get("/{operation_id}", response_model=OperationDetailDTO)
def get_operation_detail(
    operation_id: str = Path(...),
    service: OperationsService = Depends(get_operations_service),
    current_user = Depends(get_current_user)
) -> OperationDetailDTO:
    """
    Returns the read-only details of a specific operation.
    """
    return service.get_operation_detail(operation_id)
