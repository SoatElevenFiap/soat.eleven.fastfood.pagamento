from modules.external_provider.enums.external_provider_payment_status import (
    ExternalProviderPaymentStatus,
)
from modules.external_provider.models import ExternalOrderPaymentResultModel
from modules.payment.services.domain.approve_payment_service import (
    ApprovePaymentService,
)
from modules.shared.adapters import DomainService
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException


class ProcessExternalPaymentResultService(DomainService):
    def __init__(self, approve_payment_service: ApprovePaymentService):
        self.__approve_payment_service = approve_payment_service
        super().__init__(context=ProcessExternalPaymentResultService.__name__)

    async def process(self, result: ExternalOrderPaymentResultModel):
        match result.status:
            case ExternalProviderPaymentStatus.APPROVED:
                self.logger.info(
                    f"External provider payment approved, end_to_end_id: {result.end_to_end_id}"
                )
                await self.__approve_payment_service.process(result.end_to_end_id)
            case ExternalProviderPaymentStatus.REJECTED:
                self.logger.info(
                    f"External provider payment rejected, end_to_end_id: {result.end_to_end_id}"
                )
            case _:
                self.logger.error(
                    f"Invalid external provider payment status: {result.status}"
                )
                raise DomainException(
                    ExceptionConstants.INVALID_EXTERNAL_PROVIDER,
                    f"Invalid external provider payment status: {result.status}"
                )
