from abc import ABC, abstractmethod

from modules.external_provider.dataclasses import ExternalOrderDataclass


class ExternalProviderAdapter(ABC):
    @abstractmethod
    async def process_external_feedback(self, *args, **kwargs):
        """Deve processar o feedback externo (Ex:. Webhook) e atualizar o status do pedido."""
        raise NotImplementedError(
            "Method process_external_feedback must be implemented"
        )

    @abstractmethod
    async def create_order(self, *args, **kwargs) -> ExternalOrderDataclass:
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
    async def get_order(self, *args, **kwargs) -> ExternalOrderDataclass:
        """Deve retornar um pedido do provedor externo."""
        raise NotImplementedError("Method get_order must be implemented")
