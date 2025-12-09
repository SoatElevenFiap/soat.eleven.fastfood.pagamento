import json

from modules.notification.services.domain.notify_listeners_service import (
    NotifyListenersService,
)
from modules.payment.constants import PaymentCacheKeys
from modules.payment.enums import PaymentStatus
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.adapters import DomainService
from modules.shared.adapters.cache_adapter import CacheAdapter
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException


class ChangePaymentStatusService(DomainService):
    def __init__(
        self,
        notify_listeners_service: NotifyListenersService,
        payment_repository: PaymentRepository,
        cache: CacheAdapter,
    ):
        self.__notify_listeners_service = notify_listeners_service
        self.__payment_repository = payment_repository
        self.__cache = cache
        super().__init__(context=ChangePaymentStatusService.__name__)

    async def process(self, end_to_end_id: str, status: PaymentStatus):
        self.logger.info(
            f"Changing payment status to {status.value} for end_to_end_id: {end_to_end_id}"
        )
        
        payment = await self.__payment_repository.get_payment_by_end_to_end_id(
            end_to_end_id
        )
        
        if not payment:
            self.logger.error(f"Payment not found e2e_id: {end_to_end_id}")
            raise DomainException(
                ExceptionConstants.PAYMENT_NOT_FOUND,
                f"Payment not found e2e_id: {end_to_end_id}",
            )
        
        updated_payment = await self.__payment_repository.change_payment_status(
            payment.id, status
        )
        
        if updated_payment:
            payment_dict = updated_payment.model_dump(mode="json")
            if "id" in payment_dict:
                payment_dict["_id"] = payment_dict.pop("id")
            
            self.__cache.set_value(
                PaymentCacheKeys.payment_key_for(updated_payment.id),
                json.dumps(payment_dict),
            )
            
            self.__cache.set_value(
                PaymentCacheKeys.payment_by_end_to_end_id_key_for(end_to_end_id),
                json.dumps(payment_dict),
            )
            
            self.logger.info(
                f"Payment status changed to {status.value} for end_to_end_id: {end_to_end_id}"
            )
        
        await self.__notify_listeners_service.process(updated_payment)
        
        return updated_payment
