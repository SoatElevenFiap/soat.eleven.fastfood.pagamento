from typing import Annotated

from fastapi import Depends

from modules.notification.providers.notify_listeners_service_provider import (
    NotifyListenersServiceProvider,
)
from modules.payment.providers.payment_repository_provider import (
    PaymentRepositoryProvider,
)
from modules.payment.services.domain.change_payment_status_service import (
    ChangePaymentStatusService,
)
from modules.shared.providers import RedisServiceProvider


def change_payment_status_service_provider(
    notify_listeners_service: NotifyListenersServiceProvider,
    payment_repository: PaymentRepositoryProvider,
    redis_service: RedisServiceProvider,
):
    return ChangePaymentStatusService(
        notify_listeners_service=notify_listeners_service,
        payment_repository=payment_repository,
        cache=redis_service,
    )


ChangePaymentStatusServiceProvider = Annotated[
    ChangePaymentStatusService, Depends(change_payment_status_service_provider)
]
