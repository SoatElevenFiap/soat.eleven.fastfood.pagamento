from typing import Annotated

from fastapi import Depends

from modules.external_provider.services.domain.get_external_provider_service import (
    GetExternalProviderService,
)
from modules.shared.providers.mercado_pago_service_provider import (
    MercadoPagoServiceProvider,
)


def get_external_provider_service_provider(
    mercado_pago_service: MercadoPagoServiceProvider,
):
    return GetExternalProviderService(
        mercado_pago_service=mercado_pago_service,
    )


GetExternalProviderServiceProvider = Annotated[
    GetExternalProviderService, Depends(get_external_provider_service_provider)
]
