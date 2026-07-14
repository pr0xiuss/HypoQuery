from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from backend.api.dependencies import get_application_settings
from backend.platform.config.settings import Settings
from backend.platform.shared.dto.api_response import ApiResponse

router = APIRouter()


@router.get(
    "/system",
    response_model=ApiResponse[dict[str, str]],
    summary="System Information",
)
async def system_information(
    request: Request,
    settings: Settings = Depends(get_application_settings),
) -> ApiResponse[dict[str, str]]:
    """
    Returns basic application information.
    """

    return ApiResponse(
        data={
            "application": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "request_id": request.state.request_id,
        }
    )