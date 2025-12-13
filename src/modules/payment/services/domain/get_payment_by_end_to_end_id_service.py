from typing import Optional

from modules.payment.entities import PaymentEntity
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.adapters import DomainService


class GetPaymentByEndToEndIdService(DomainService):
    def __init__(self, payment_repository: PaymentRepository):
        self.__payment_repository = payment_repository
        super().__init__(context=GetPaymentByEndToEndIdService.__name__)

    async def process(self, end_to_end_id: str) -> Optional[PaymentEntity]:
        self.logger.info(f"Getting payment by end_to_end_id: {end_to_end_id}")
        return await self.__payment_repository.get_payment_by_end_to_end_id(end_to_end_id)
        
