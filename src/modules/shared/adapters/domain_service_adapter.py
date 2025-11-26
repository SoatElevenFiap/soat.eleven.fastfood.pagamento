from abc import ABC, abstractmethod
from typing import Optional

from modules.shared.services.logger.logger_service import LoggerService


class DomainService(ABC):
    def __init__(self, context: Optional[str] = "Logger"):
        self.logger = LoggerService(context)

    @abstractmethod
    def process(self, *args, **kwargs):
        raise NotImplementedError("Método process deve ser implementado")
