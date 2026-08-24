from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.api.dependencies.auth import get_current_user
from backend.knowledge.service import ContextService, ExplanationService
from backend.knowledge.context import ContextContext
from backend.knowledge.context_state.job import ContextJob
from backend.knowledge.explanation import ExplanationContext
from backend.knowledge.explanation_state.job import ExplanationJob

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

class BuildContextRequest(BaseModel):
    query_id: str
    optimization_snapshot_id: str

class ExplainRequest(BaseModel):
    query_id: str
    optimization_snapshot_id: str

from backend.api.dependencies.product import get_context_service, get_explanation_service

@router.post("/context", response_model=dict)
def build_context(
    request: BuildContextRequest,
    service: ContextService = Depends(get_context_service),
    current_user = Depends(get_current_user),
):
    """
    Builds the optimization context.
    """
    job = ContextJob(
        query_id=request.query_id,
        optimization_snapshot_id=request.optimization_snapshot_id
    )
    context = ContextContext(job=job)
    snapshot = service.build(context)
    
    # Return as dict for now until we define a specific DTO
    # FastAPI handles dataclass serialization implicitly if configured, 
    # but normally we map this to a Pydantic DTO.
    return {"snapshot_id": "temp"} # Placeholder return

@router.post("/explain", response_model=dict)
def explain(
    request: ExplainRequest,
    service: ExplanationService = Depends(get_explanation_service),
    current_user = Depends(get_current_user),
):
    """
    Builds an explanation from the optimization context.
    """
    job = ExplanationJob(
        query_id=request.query_id,
        optimization_snapshot_id=request.optimization_snapshot_id
    )
    context = ExplanationContext(job=job)
    snapshot = service.explain(context)
    
    return {"snapshot_id": "temp"} # Placeholder return
