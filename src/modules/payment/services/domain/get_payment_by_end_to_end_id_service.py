import json
from typing import Optional

from modules.payment.constants import PaymentCacheKeys
from modules.payment.entities import PaymentEntity
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.adapters import DomainService
from modules.shared.adapters.cache_adapter import CacheAdapter


class GetPaymentByEndToEndIdService(DomainService):
    def __init__(self, cache: CacheAdapter, payment_repository: PaymentRepository):
        self.__payment_repository = payment_repository
        self.__cache = cache
        super().__init__(context=GetPaymentByEndToEndIdService.__name__)

    async def process(self, end_to_end_id: str) -> Optional[PaymentEntity]:
        self.logger.info(f"Getting payment by end_to_end_id: {end_to_end_id}")
        
        cache_key = PaymentCacheKeys.payment_by_end_to_end_id_key_for(end_to_end_id)
        cached_data = self.__cache.get_value(cache_key)
        
        if cached_data:
            self.logger.info(f"Payment found in cache for end_to_end_id: {end_to_end_id}")
            return PaymentEntity(**json.loads(cached_data))
        
        payment = await self.__payment_repository.get_payment_by_end_to_end_id(end_to_end_id)
        
        if payment:
            payment_dict = payment.model_dump(mode="json")
            if "id" in payment_dict:
                payment_dict["_id"] = payment_dict.pop("id")
            self.__cache.set_value(
                cache_key,
                json.dumps(payment_dict),
            )
            self.__cache.set_value(
                PaymentCacheKeys.payment_key_for(payment.id),
                json.dumps(payment_dict),
            )
            self.logger.info(f"Payment found and cached for end_to_end_id: {end_to_end_id}")
            return payment
        
        self.logger.warning(f"Payment not found for end_to_end_id: {end_to_end_id}")
        return None
