import json

from modules.notification.services.domain.notify_listeners_service import (
    NotifyListenersService,
)
from modules.payment.constants import PaymentCacheKeys
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.adapters import DomainService
from modules.shared.adapters.cache_adapter import CacheAdapter
from modules.shared.exceptions.domain_exception import DomainException


class ApprovePaymentService(DomainService):
    def __init__(
        self,
        notify_listeners_service: NotifyListenersService,
        payment_repository: PaymentRepository,
        cache: CacheAdapter,
    ):
        self.__notify_listeners_service = notify_listeners_service
        self.__payment_repository = payment_repository
        self.__cache = cache
        super().__init__(context=ApprovePaymentService.__name__)

    async def process(self, end_to_end_id: str):
        self.logger.info("Approving payment...")
        payment = await self.__payment_repository.get_payment_by_end_to_end_id(
            end_to_end_id
        )
        if not payment:
            self.logger.error(f"Payment not found e2e_id: {end_to_end_id}")
            raise DomainException(f"Payment not found e2e_id: {end_to_end_id}")
        payment = await self.__payment_repository.make_payment_paid(payment.id)
        if payment:
            payment_dict = payment.model_dump(mode="json")
            if "id" in payment_dict:
                payment_dict["_id"] = payment_dict.pop("id")
            self.__cache.set_value(
                PaymentCacheKeys.payment_key_for(payment.id),
                json.dumps(payment_dict),
            )
        await self.__notify_listeners_service.process(payment)
        return payment
