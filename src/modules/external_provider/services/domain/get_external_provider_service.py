from modules.external_provider.adapters import ExternalProviderAdapter
from modules.external_provider.enums import ExternalProvider
from modules.shared.adapters import DomainService
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException
from modules.shared.providers.mercado_pago_service_provider import (
    MercadoPagoServiceProvider,
)


class GetExternalProviderService(DomainService):
    def __init__(self, mercado_pago_service: MercadoPagoServiceProvider):
        self.__mercado_pago_service = mercado_pago_service
        super().__init__(context=GetExternalProviderService.__name__)

    async def process(
        self, provider: ExternalProvider | str
    ) -> ExternalProviderAdapter:
        self.logger.info("Getting external provider...")
        match provider:
            case ExternalProvider.MERCADOPAGO:
                return self.__mercado_pago_service
            case _:
                raise DomainException(
                    ExceptionConstants.INVALID_EXTERNAL_PROVIDER,
                    f"Provider {provider} not supported or disabled",
                )
