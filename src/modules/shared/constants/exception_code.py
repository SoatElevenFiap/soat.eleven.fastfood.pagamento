from typing import NamedTuple


class ExceptionCode(NamedTuple):
    status_code: int
    code: str


class ExceptionConstants:
    CLIENT_ALREADY_EXISTS = ExceptionCode(409, "CLIENT_ALREADY_EXISTS")
    PAYMENT_ALREADY_EXISTS = ExceptionCode(409, "PAYMENT_ALREADY_EXISTS")
    PAYMENT_NOT_FOUND = ExceptionCode(404, "PAYMENT_NOT_FOUND")
    INVALID_EXTERNAL_PROVIDER = ExceptionCode(400, "INVALID_EXTERNAL_PROVIDER")
    INVALID_CLIENT = ExceptionCode(400, "INVALID_CLIENT")
    CLIENT_NOT_FOUND = ExceptionCode(404, "CLIENT_NOT_FOUND")
    INVALID_REQUEST = ExceptionCode(400, "INVALID_REQUEST")
