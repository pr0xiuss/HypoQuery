from pydantic import BaseModel
from pydantic import ConfigDict


class LogoutResponse(BaseModel):
    """
    Response returned after logout.
    """

    message: str

    model_config = ConfigDict(
        frozen=True,
    )