from abc import ABC, abstractmethod
from datetime import UTC, datetime
from typing import Any, Dict

from modules.external_provider.dtos import ExternalOrderResultDto
from modules.external_provider.entities import ExternalOrderEntity
from modules.external_provider.models import (
    CreateExternalOrderModel,
    ExternalOrderPaymentResultModel,
)
from modules.external_provider.repositories.external_provider_repository import (
    ExternalProviderRepository,
)


class ExternalProviderAdapter(ABC):
    def __init__(self, external_provider_repository: ExternalProviderRepository):
        self.__external_provider_repository = external_provider_repository
        super().__init__()

    @abstractmethod
    async def process_external_feedback(
        self, *args, **kwargs
    ) -> ExternalOrderPaymentResultModel:
        """Deve processar o feedback externo (Ex:. Webhook) e atualizar o status do pedido."""
        raise NotImplementedError(
            "Method process_external_feedback must be implemented"
        )

    @abstractmethod
    async def create_order(
        self, request: CreateExternalOrderModel
    ) -> ExternalOrderEntity:
        """Deve criar um pedido no provedor externo."""
        raise NotImplementedError("Method create_order must be implemented")

    @abstractmethod
    async def cancel_order(self, *args, **kwargs):
        """Deve cancelar um pedido no provedor externo."""
        raise NotImplementedError("Method cancel_order must be implemented")

    @abstractmethod
    async def refund_order(self, *args, **kwargs):
        """Deve reembolsar um pedido no provedor externo."""
        raise NotImplementedError("Method refund_order must be implemented")

    @abstractmethod
    async def get_order(self, *args, **kwargs) -> ExternalOrderResultDto:
        """Deve retornar um pedido do provedor externo."""
        raise NotImplementedError("Method get_order must be implemented")

    async def add_external_provider_request(
        self,
        end_to_end_id: str,
        external_reference_id: str,
        request: Dict[str, Any],
        response: Dict[str, Any],
    ):
        return await self.__external_provider_repository.add_external_provider_request(
            {
                "external_reference_id": external_reference_id,
                "end_to_end_id": end_to_end_id,
                "request": request,
                "response": response,
                "created_at": datetime.now(UTC).isoformat(),
            }
        )
