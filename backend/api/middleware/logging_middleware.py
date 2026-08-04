import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from backend.platform.shared.request_context import generate_request_id
from backend.platform.shared.request_context import set_request_id
from backend.shared.logger import get_logger


logger = get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every incoming HTTP request and its corresponding response.
    """

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        request_id = generate_request_id()

        set_request_id(request_id)

        request.state.request_id = request_id

        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * 1000

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "[%s] %s %s | %d | %.2f ms",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response