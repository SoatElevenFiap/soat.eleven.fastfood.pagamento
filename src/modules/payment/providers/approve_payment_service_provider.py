from typing import Annotated

from fastapi import Depends

from modules.notification.providers.notify_listeners_service_provider import (
    NotifyListenersServiceProvider,
)
from modules.payment.providers.payment_repository_provider import (
    PaymentRepositoryProvider,
)
from modules.payment.services.domain.approve_payment_service import (
    ApprovePaymentService,
)


def approve_payment_service_provider(
    notify_listeners_service: NotifyListenersServiceProvider,
    payment_repository: PaymentRepositoryProvider,
):
    return ApprovePaymentService(
        notify_listeners_service=notify_listeners_service,
        payment_repository=payment_repository,
    )


ApprovePaymentServiceProvider = Annotated[
    ApprovePaymentService, Depends(approve_payment_service_provider)
]
