from typing import Annotated

from fastapi import Depends

from modules.payment.providers.get_payment_by_end_to_end_id_service import (
    GetPaymentByEndToEndIdServiceProvider,
)
from modules.payment.providers.get_payment_service_provider import (
    GetPaymentServiceProvider,
)
from modules.payment.services.application.get_payment_service import (
    GetPaymentApplicationService,
)


def get_payment_application_service_provider(
    get_payment_service: GetPaymentServiceProvider,
    get_payment_by_end_to_end_id_service: GetPaymentByEndToEndIdServiceProvider,
):
    return GetPaymentApplicationService(
        get_payment_service=get_payment_service,
        get_payment_by_end_to_end_id_service=get_payment_by_end_to_end_id_service,
    )


GetPaymentApplicationServiceProvider = Annotated[
    GetPaymentApplicationService, Depends(get_payment_application_service_provider)
]
