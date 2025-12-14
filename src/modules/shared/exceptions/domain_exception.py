from typing import Optional

from modules.shared.constants import ExceptionCode


class DomainException(Exception):
    def __init__(self, code: ExceptionCode, message: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(message)
