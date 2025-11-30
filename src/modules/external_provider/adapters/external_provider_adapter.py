from abc import ABC, abstractmethod

from modules.external_provider.enums.external_provider_payment_status import ExternalProviderPaymentStatus


class ExternalProviderAdapter(ABC):
    @abstractmethod
    def get_payment_status(self, *args, **kwargs) -> ExternalProviderPaymentStatus:
        """Deve retornar o status do pagamento baseado no enum `ExternalProviderPaymentStatus`"""
        raise NotImplementedError("Method get_payment_status must be implemented")

    @abstractmethod
    def process_external_feedback(self, *args, **kwargs):
        """Deve processar o feedback externo (Ex:. Webhook) e atualizar o status do pagamento."""
        raise NotImplementedError("Method process_external_feedback must be implemented")

    @abstractmethod
    def create_payment(self, *args, **kwargs):
        """Deve criar um pagamento no provedor externo."""
        raise NotImplementedError("Method create_payment must be implemented")

    @abstractmethod
    def cancel_payment(self, *args, **kwargs):
        """Deve cancelar um pagamento no provedor externo."""
        raise NotImplementedError("Method cancel_payment must be implemented")

    @abstractmethod
    def refund_payment(self, *args, **kwargs):
        """Deve reembolsar um pagamento no provedor externo."""
        raise NotImplementedError("Method refund_payment must be implemented")

    @abstractmethod
    def get_payment(self, *args, **kwargs):
        """Deve retornar um pagamento do provedor externo."""
        raise NotImplementedError("Method get_payment must be implemented")