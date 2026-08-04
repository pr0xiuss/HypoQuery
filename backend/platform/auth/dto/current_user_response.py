from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class CurrentUserResponse(BaseModel):
    """
    Response DTO for the currently authenticated user.
    """

    id: UUID

    username: str

    email: EmailStr

    is_active: bool

    is_verified: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        frozen=True,
    )