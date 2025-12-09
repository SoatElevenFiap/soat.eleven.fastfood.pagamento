from typing import Annotated

from fastapi import Depends

from modules.payment.providers.change_payment_status_service_provider import (
    ChangePaymentStatusServiceProvider,
)
from modules.webhook.services.domain.process_external_payment_result_service import (
    ProcessExternalPaymentResultService,
)


def process_external_payment_result_service_provider(
    change_payment_status_service: ChangePaymentStatusServiceProvider,
):
    return ProcessExternalPaymentResultService(
        change_payment_status_service=change_payment_status_service
    )


ProcessExternalPaymentResultServiceProvider = Annotated[
    ProcessExternalPaymentResultService,
    Depends(process_external_payment_result_service_provider),
]
