from fastapi import APIRouter
from fastapi import Depends

from backend.api.dependencies import get_current_user
from backend.platform.auth.domain.user import User
from backend.platform.auth.dto.current_user_response import (
    CurrentUserResponse,
)

router = APIRouter(
    prefix="/users",
)


@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_user,
    ),
) -> CurrentUserResponse:
    """
    Returns the currently authenticated user.
    """

    return CurrentUserResponse.model_validate(
        current_user.model_dump(),
    )