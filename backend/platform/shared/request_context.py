from contextvars import ContextVar
from uuid import uuid4


_request_id: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)


def set_request_id(request_id: str) -> None:
    """
    Stores the current request ID.
    """
    _request_id.set(request_id)


def get_request_id() -> str | None:
    """
    Returns the current request ID.
    """
    return _request_id.get()


def generate_request_id() -> str:
    """
    Generates a new unique request ID.
    """
    return str(uuid4())