from typing import Annotated

from fastapi import Depends

from modules.notification.providers.notify_listeners_service_provider import (
    NotifyListenersServiceProvider,
)
from modules.payment.providers.get_payment_by_end_to_end_id_service import (
    GetPaymentByEndToEndIdServiceProvider,
)
from modules.payment.providers.payment_repository_provider import (
    PaymentRepositoryProvider,
)
from modules.payment.services.domain.change_payment_status_service import (
    ChangePaymentStatusService,
)


def change_payment_status_service_provider(
    notify_listeners_service: NotifyListenersServiceProvider,
    payment_repository: PaymentRepositoryProvider,
    get_payment_by_end_to_end_id_service: GetPaymentByEndToEndIdServiceProvider,
):
    return ChangePaymentStatusService(
        notify_listeners_service=notify_listeners_service,
        payment_repository=payment_repository,
        get_payment_by_end_to_end_id_service=get_payment_by_end_to_end_id_service,
    )


ChangePaymentStatusServiceProvider = Annotated[
    ChangePaymentStatusService, Depends(change_payment_status_service_provider)
]
