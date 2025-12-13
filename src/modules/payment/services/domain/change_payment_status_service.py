
from modules.notification.services.domain.notify_listeners_service import (
    NotifyListenersService,
)
from modules.payment.enums import PaymentStatus
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.payment.services.domain.get_payment_by_end_to_end_id_service import GetPaymentByEndToEndIdService
from modules.shared.adapters import DomainService
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException


class ChangePaymentStatusService(DomainService):
    def __init__(
        self,
        notify_listeners_service: NotifyListenersService,
        payment_repository: PaymentRepository,
        get_payment_by_end_to_end_id_service: GetPaymentByEndToEndIdService,
    ):
        self.__notify_listeners_service = notify_listeners_service
        self.__payment_repository = payment_repository
        self.__get_payment_by_end_to_end_id_service = get_payment_by_end_to_end_id_service
        super().__init__(context=ChangePaymentStatusService.__name__)

    async def process(self, end_to_end_id: str, status: PaymentStatus):
        self.logger.info(
            f"Changing payment status to {status.value} for end_to_end_id: {end_to_end_id}"
        )
        
        payment = await self.__get_payment_by_end_to_end_id_service.process(
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
            self.logger.info(
                f"Payment status changed to {status.value} for end_to_end_id: {end_to_end_id}"
            )
            await self.__notify_listeners_service.process(payment)
        
        return updated_payment
