from fastapi import APIRouter

from backend.platform.shared.dto.api_response import ApiResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=ApiResponse[dict[str, str]],
    summary="Application Health",
)
async def health() -> ApiResponse[dict[str, str]]:
    """
    General application health endpoint.
    """

    return ApiResponse(
        data={
            "status": "healthy",
        }
    )


@router.get(
    "/live",
    response_model=ApiResponse[dict[str, str]],
    summary="Liveness Probe",
)
async def live() -> ApiResponse[dict[str, str]]:
    """
    Kubernetes liveness probe.
    """

    return ApiResponse(
        data={
            "status": "alive",
        }
    )


@router.get(
    "/ready",
    response_model=ApiResponse[dict[str, str]],
    summary="Readiness Probe",
)
async def ready() -> ApiResponse[dict[str, str]]:
    """
    Kubernetes readiness probe.
    """

    return ApiResponse(
        data={
            "status": "ready",
        }
    )