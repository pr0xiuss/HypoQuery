from fastapi import APIRouter

from backend.platform.apis.api.api_router import router as api_management_router

router = APIRouter()

router.include_router(
    api_management_router,
)