from fastapi import Request
from fastapi.responses import JSONResponse

from modules.shared.exceptions.application_exception import ApplicationException


def application_exception_handler(request: Request, exc: ApplicationException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message, "status": exc.status_code},
    )
