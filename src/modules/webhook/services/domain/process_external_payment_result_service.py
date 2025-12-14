from modules.external_provider.models import ExternalOrderPaymentResultModel
from modules.payment.services.domain.change_payment_status_service import (
    ChangePaymentStatusService,
)
from modules.shared.adapters import DomainService


class ProcessExternalPaymentResultService(DomainService):
    def __init__(self, change_payment_status_service: ChangePaymentStatusService):
        self.__change_payment_status_service = change_payment_status_service
        super().__init__(context=ProcessExternalPaymentResultService.__name__)

    async def process(self, result: ExternalOrderPaymentResultModel):
        await self.__change_payment_status_service.process(
            result.end_to_end_id, result.status
        )
