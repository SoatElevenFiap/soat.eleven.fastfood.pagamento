from fastapi import Request
from fastapi.responses import JSONResponse

from modules.shared.exceptions.domain_exception import DomainException


def domain_exception_handler(request: Request, exc: DomainException):
    """
    Handler para DomainException.
    Retorna o status code e código definidos no ExceptionCode,
    junto com a mensagem da exceção.
    """
    return JSONResponse(
        status_code=exc.code.status_code,
        content={
            "code": exc.code.code,
            "message": exc.message or "Domain error occurred",
        },
    )
