import uuid
from contextvars import ContextVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


class CorrelationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = str(uuid.uuid4())[:8]
        correlation_id_var.set(correlation_id)
        response: Response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        return response


def get_correlation_id() -> str:
    return correlation_id_var.get()
