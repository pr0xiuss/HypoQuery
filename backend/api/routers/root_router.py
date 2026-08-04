from fastapi import APIRouter
from fastapi import Depends

from backend.api.dependencies import get_application_settings
from backend.platform.config.settings import Settings
from backend.platform.shared.dto.api_response import ApiResponse

router = APIRouter()


@router.get(
    "/",
    response_model=ApiResponse[dict[str, str]],
    summary="API Root",
)
async def root(
    settings: Settings = Depends(get_application_settings),
) -> ApiResponse[dict[str, str]]:
    """
    Root endpoint for the HypoQuery API.
    """

    return ApiResponse(
        data={
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
        }
    )