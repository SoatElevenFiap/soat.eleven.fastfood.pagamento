from typing import Optional

from modules.payment.entities import PaymentEntity
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.adapters import DomainService


class GetPaymentService(DomainService):
    def __init__(self, payment_repository: PaymentRepository):
        self.__payment_repository = payment_repository
        super().__init__(context=GetPaymentService.__name__)

    async def process(self, payment_id: str) -> Optional[PaymentEntity]:
        self.logger.info(f"Getting payment: {payment_id}")
        return await self.__payment_repository.get_payment(payment_id)

