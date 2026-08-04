from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class User(BaseModel):
    """
    Represents a platform user.
    """

    id: UUID

    username: str

    email: EmailStr

    password_hash: str

    is_active: bool

    is_verified: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )