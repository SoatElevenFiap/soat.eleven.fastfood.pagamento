from typing import Annotated

from fastapi import Depends

from modules.external_provider.providers.external_provider_repository_provider import (
    ExternalProviderRepositoryProvider,
)
from modules.shared.providers.settings_provider import SettingsProvider
from modules.shared.services.mercadopago.mercado_pago_service import (
    MercadoPagoCredentials,
    MercadoPagoService,
)


def mercado_pago_service_provider(
    settings: SettingsProvider,
    external_provider_repository: ExternalProviderRepositoryProvider,
):
    return MercadoPagoService(
        credentials=MercadoPagoCredentials(
            access_token=settings.mercado_pago_access_token
        ),
        external_provider_repository=external_provider_repository,
    )


MercadoPagoServiceProvider = Annotated[
    MercadoPagoService, Depends(mercado_pago_service_provider)
]
