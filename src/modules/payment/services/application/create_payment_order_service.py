
from modules.client.providers.get_client_service_provider import (
    GetClientServiceProvider,
)
from modules.external_provider.models import CreateExternalOrderModel
from modules.external_provider.providers.get_external_provider_service_provider import (
    GetExternalProviderServiceProvider,
)
from modules.payment.dtos import CreatePaymentOrderRequestDto
from modules.payment.dtos.payment_dto import PaymentDto
from modules.payment.providers.create_payment_service import (
    CreatePaymentServiceProvider,
)
from modules.shared.adapters import ApplicationService
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException


class CreatePaymentOrderService(ApplicationService):
    def __init__(
        self,
        get_client_service: GetClientServiceProvider,
        get_external_provider_service: GetExternalProviderServiceProvider,
        create_payment_service: CreatePaymentServiceProvider,
    ):
        self.__get_client_service = get_client_service
        self.__get_external_provider_service = get_external_provider_service
        self.__create_payment_service = create_payment_service
        super().__init__(context=CreatePaymentOrderService.__name__)

    async def process(self, request: CreatePaymentOrderRequestDto) -> PaymentDto:
        self.logger.info(
            f"Creating payment order for client: {request.client_id} and end_to_end_id: {request.end_to_end_id}"
        )
        client = await self.__get_client_service.process(request.client_id)
        if not client:
            self.logger.error(f"Client not found: {request.client_id}")
            raise DomainException(ExceptionConstants.CLIENT_NOT_FOUND, f"Client not found for id: {request.client_id}")
        external_provider_service = await self.__get_external_provider_service.process(
            request.provider
        )
        order = await external_provider_service.create_order(
            CreateExternalOrderModel(
                client_id=request.client_id,
                end_to_end_id=request.end_to_end_id,
                items=request.items,
            )
        )
        payment = await self.__create_payment_service.process(order)
        return PaymentDto.from_payment_entity(payment)
