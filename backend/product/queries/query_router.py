from fastapi import APIRouter, Depends, Query, Path
from backend.product.queries.dtos import ListQueriesResponse, QueryDetailDTO
from backend.product.queries.query_service import QueryService
from backend.api.dependencies.auth import get_current_user
from typing import Optional

router = APIRouter(prefix="/queries", tags=["Queries"])

from backend.api.dependencies.product import get_query_service

@router.get("/", response_model=ListQueriesResponse)
def list_queries(
    fingerprint_id: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    service: QueryService = Depends(get_query_service),
    current_user = Depends(get_current_user)
) -> ListQueriesResponse:
    """
    Returns a product view of queries based on execution and history data.
    """
    return service.list_queries(fingerprint_id=fingerprint_id, limit=limit, offset=offset)

@router.get("/{query_id}", response_model=QueryDetailDTO)
def get_query_detail(
    query_id: str = Path(...),
    service: QueryService = Depends(get_query_service),
    current_user = Depends(get_current_user)
) -> QueryDetailDTO:
    """
    Returns a cohesive detailed view of a query, including its optimization state.
    """
    return service.get_query_detail(query_id)
