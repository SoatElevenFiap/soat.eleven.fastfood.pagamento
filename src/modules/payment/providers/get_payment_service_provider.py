from typing import Annotated

from fastapi import Depends

from modules.payment.providers.payment_repository_provider import (
    PaymentRepositoryProvider,
)
from modules.payment.services.domain.get_payment_service import GetPaymentService


def get_payment_service_provider(
    payment_repository: PaymentRepositoryProvider,
):
    return GetPaymentService(payment_repository=payment_repository)


GetPaymentServiceProvider = Annotated[
    GetPaymentService, Depends(get_payment_service_provider)
]
