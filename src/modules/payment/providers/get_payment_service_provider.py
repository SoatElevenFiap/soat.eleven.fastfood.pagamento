from typing import Annotated

from fastapi import Depends

from modules.payment.providers.payment_repository_provider import (
    PaymentRepositoryProvider,
)
from modules.payment.services.domain.get_payment_service import GetPaymentService
from modules.shared.providers import RedisServiceProvider


def get_payment_service_provider(
    redis_service: RedisServiceProvider,
    payment_repository: PaymentRepositoryProvider,
):
    return GetPaymentService(cache=redis_service, payment_repository=payment_repository)


GetPaymentServiceProvider = Annotated[
    GetPaymentService, Depends(get_payment_service_provider)
]

