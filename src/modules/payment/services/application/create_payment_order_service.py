from fastapi import HTTPException

from modules.client.providers.get_client_service_provider import (
    GetClientServiceProvider,
)
from modules.external_provider.models import CreateExternalOrderModel
from modules.external_provider.providers.get_external_provider_service_provider import (
    GetExternalProviderServiceProvider,
)
from modules.payment.dtos import CreatePaymentOrderRequestDto
from modules.payment.entities import PaymentEntity
from modules.payment.providers.create_payment_service import (
    CreatePaymentServiceProvider,
)
from modules.shared.adapters import ApplicationService


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

    async def process(self, request: CreatePaymentOrderRequestDto) -> PaymentEntity:
        self.logger.info(
            f"Creating payment order for client: {request.client_id} and end_to_end_id: {request.end_to_end_id}"
        )
        client = await self.__get_client_service.process(request.client_id)
        if not client:
            self.logger.error(f"Client not found: {request.client_id}")
            raise HTTPException(status_code=404, detail="Client not found")
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
        return payment
