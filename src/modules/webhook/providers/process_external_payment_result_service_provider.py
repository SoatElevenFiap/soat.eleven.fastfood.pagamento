from typing import Annotated

from fastapi import Depends

from modules.payment.providers.approve_payment_service_provider import (
    ApprovePaymentServiceProvider,
)
from modules.webhook.services.domain.process_external_payment_result_service import (
    ProcessExternalPaymentResultService,
)


def process_external_payment_result_service_provider(
    approve_payment_service: ApprovePaymentServiceProvider,
):
    return ProcessExternalPaymentResultService(
        approve_payment_service=approve_payment_service
    )


ProcessExternalPaymentResultServiceProvider = Annotated[
    ProcessExternalPaymentResultService,
    Depends(process_external_payment_result_service_provider),
]
