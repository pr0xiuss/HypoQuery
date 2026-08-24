from fastapi import APIRouter, Depends
from pydantic import BaseModel

from backend.assistant.contracts.assistant_request import AssistantRequest
from backend.assistant.contracts.assistant_response import AssistantResponse
from backend.assistant.api.assistant_service_facade import AssistantServiceFacade
from backend.api.dependencies.auth import get_current_user

router = APIRouter(prefix="/assistant", tags=["Assistant"])

from backend.api.dependencies.product import get_assistant_facade

@router.post("/explain", response_model=AssistantResponse)
def explain(
    request: AssistantRequest,
    facade: AssistantServiceFacade = Depends(get_assistant_facade),
    current_user = Depends(get_current_user),
) -> AssistantResponse:
    """
    Exposes the assistant explanation capability.
    """
    return facade.explain(request)
