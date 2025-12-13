from typing import Optional

from modules.payment.dtos.payment_dto import PaymentDto
from modules.payment.providers.get_payment_by_end_to_end_id_service import (
    GetPaymentByEndToEndIdServiceProvider,
)
from modules.payment.providers.get_payment_service_provider import (
    GetPaymentServiceProvider,
)
from modules.shared.adapters import ApplicationService
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException


class GetPaymentApplicationService(ApplicationService):
    def __init__(
        self,
        get_payment_service: GetPaymentServiceProvider,
        get_payment_by_end_to_end_id_service: GetPaymentByEndToEndIdServiceProvider,
    ):
        self.__get_payment_service = get_payment_service
        self.__get_payment_by_end_to_end_id_service = get_payment_by_end_to_end_id_service
        super().__init__(context=GetPaymentApplicationService.__name__)

    async def process(
        self, id: Optional[str] = None, end_to_end_id: Optional[str] = None
    ) -> PaymentDto:
        if not id and not end_to_end_id:
            raise DomainException(
                ExceptionConstants.INVALID_REQUEST,
                "Either 'id' or 'end_to_end_id' parameter must be provided",
            )

        if id and end_to_end_id:
            raise DomainException(
                ExceptionConstants.INVALID_REQUEST,
                "Only one parameter ('id' or 'end_to_end_id') should be provided",
            )

        if id:
            self.logger.info(f"Getting payment by id: {id}")
            payment = await self.__get_payment_service.process(id)
            if not payment:
                self.logger.error(f"Payment not found for id: {id}")
                raise DomainException(
                    ExceptionConstants.PAYMENT_NOT_FOUND,
                    f"Payment not found for id: {id}",
                )
            return PaymentDto.from_payment_entity(payment)

        self.logger.info(f"Getting payment by end_to_end_id: {end_to_end_id}")
        payment = await self.__get_payment_by_end_to_end_id_service.process(end_to_end_id)
        if not payment:
            self.logger.error(f"Payment not found for end_to_end_id: {end_to_end_id}")
            raise DomainException(
                ExceptionConstants.PAYMENT_NOT_FOUND,
                f"Payment not found for end_to_end_id: {end_to_end_id}",
            )
        return PaymentDto.from_payment_entity(payment)
