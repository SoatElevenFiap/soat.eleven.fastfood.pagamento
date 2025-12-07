from modules.payment.entities.payment_entity import PaymentEntity
from modules.payment.providers.payment_repository_provider import (
    PaymentRepositoryProvider,
)
from modules.shared.adapters import InfraService


class PaymentService(InfraService):
    def __init__(self, payment_repository: PaymentRepositoryProvider):
        self.__payment_repository = payment_repository
        super().__init__(PaymentService.__name__)

    def create_payment(self) -> PaymentEntity:
        pass
