import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def global_exception_handler(request: Request, exc: Exception):
    """
    Handler global para exceções não mapeadas.
    Retorna status code 500 com código INTERNAL_ERROR.
    """
    logger.error(
        f"Unhandled exception: {type(exc).__name__} - {str(exc)}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_ERROR",
            "message": "Internal server error",
        },
    )
