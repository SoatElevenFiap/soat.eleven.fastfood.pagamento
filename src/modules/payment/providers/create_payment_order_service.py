from typing import Annotated

from fastapi import Depends

from modules.client.providers.get_client_service_provider import (
    GetClientServiceProvider,
)
from modules.external_provider.providers.get_external_provider_service_provider import (
    GetExternalProviderServiceProvider,
)
from modules.payment.providers.create_payment_service import (
    CreatePaymentServiceProvider,
)
from modules.payment.services.application.create_payment_order_service import (
    CreatePaymentOrderService,
)


def get_create_payment_order_service_provider(
    get_client_service: GetClientServiceProvider,
    get_external_provider_service: GetExternalProviderServiceProvider,
    create_payment_service: CreatePaymentServiceProvider,
):
    return CreatePaymentOrderService(
        get_client_service=get_client_service,
        get_external_provider_service=get_external_provider_service,
        create_payment_service=create_payment_service,
    )


CreatePaymentOrderServiceProvider = Annotated[
    CreatePaymentOrderService, Depends(get_create_payment_order_service_provider)
]
