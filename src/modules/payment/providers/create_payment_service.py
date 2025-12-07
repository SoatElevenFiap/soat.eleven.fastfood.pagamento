from typing import Annotated

from fastapi import Depends

from modules.payment.providers.payment_repository_provider import (
    PaymentRepositoryProvider,
)
from modules.payment.services.domain.create_payment_service import CreatePaymentService


def create_payment_service_provider(payment_repository: PaymentRepositoryProvider):
    return CreatePaymentService(payment_repository=payment_repository)


CreatePaymentServiceProvider = Annotated[
    CreatePaymentService, Depends(create_payment_service_provider)
]
