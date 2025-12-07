import json
from typing import Optional

from modules.payment.constants import PaymentCacheKeys
from modules.payment.entities import PaymentEntity
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.adapters import DomainService
from modules.shared.adapters.cache_adapter import CacheAdapter


class GetPaymentService(DomainService):
    def __init__(self, cache: CacheAdapter, payment_repository: PaymentRepository):
        self.__payment_repository = payment_repository
        self.__cache = cache
        super().__init__(context=GetPaymentService.__name__)

    async def process(self, payment_id: str) -> Optional[PaymentEntity]:
        self.logger.info(f"Getting payment: {payment_id}")
        cached_data = self.__cache.get_value(
            PaymentCacheKeys.payment_key_for(payment_id)
        )
        if cached_data:
            return PaymentEntity(**json.loads(cached_data))
        payment = await self.__payment_repository.get_payment(payment_id)
        if payment:
            payment_dict = payment.model_dump(mode="json")
            if "id" in payment_dict:
                payment_dict["_id"] = payment_dict.pop("id")
            self.__cache.set_value(
                PaymentCacheKeys.payment_key_for(payment_id),
                json.dumps(payment_dict),
            )
            return payment
        return None

