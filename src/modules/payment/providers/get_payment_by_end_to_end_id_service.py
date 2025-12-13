from typing import Annotated

from fastapi import Depends

from modules.payment.providers.payment_repository_provider import (
    PaymentRepositoryProvider,
)
from modules.payment.services.domain.get_payment_by_end_to_end_id_service import (
    GetPaymentByEndToEndIdService,
)


def get_payment_by_end_to_end_id_service_provider(
    payment_repository: PaymentRepositoryProvider,
):
    return GetPaymentByEndToEndIdService(payment_repository=payment_repository)


GetPaymentByEndToEndIdServiceProvider = Annotated[
    GetPaymentByEndToEndIdService,
    Depends(get_payment_by_end_to_end_id_service_provider),
]
