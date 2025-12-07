from mercadopago import SDK
from pydantic import BaseModel

from modules.external_provider.adapters import ExternalProviderAdapter
from modules.external_provider.entities import ExternalOrderEntity
from modules.external_provider.enums import ExternalProvider
from modules.external_provider.enums.external_provider_payment_status import (
    ExternalProviderPaymentStatus,
)
from modules.external_provider.models import (
    CreateExternalOrderModel,
    ExternalOrderPaymentResultModel,
)
from modules.external_provider.repositories.external_provider_repository import (
    ExternalProviderRepository,
)
from modules.shared.exceptions.domain_exception import DomainException
from modules.shared.services.logger.logger_service import LoggerService
from modules.shared.services.mercadopago.dataclasses import PaymentNotificationDataclass


class MercadoPagoCredentials(BaseModel):
    access_token: str
    sandbox: bool = False


class MercadoPagoService(ExternalProviderAdapter):
    def __init__(
        self,
        credentials: MercadoPagoCredentials,
        external_provider_repository: ExternalProviderRepository,
    ):
        self.__sdk = SDK(credentials.access_token)
        self.__preference = self.__sdk.preference()
        self.logger = LoggerService(context="MercadoPagoService")
        super().__init__(external_provider_repository=external_provider_repository)

    async def create_order(
        self, request: CreateExternalOrderModel
    ) -> ExternalOrderEntity:
        self.logger.info("Creating order...")
        items = [item.model_dump() for item in request.items]
        total_amount = sum(
            float(item["unit_price"]) * float(item["quantity"]) for item in items
        )
        preference = self.__preference.create(
            {
                "items": items,
                "external_reference": request.end_to_end_id,
                "total_amount": total_amount,
                "payment_methods": {
                    "excluded_payment_types": [{"id": "ticket"}],
                    "default_payment_method_id": "visa",
                    "installments": 1,
                },
                "notification_url": "https://prokicon.free.beeceptor.com",
            }
        )
        status = (
            ExternalProviderPaymentStatus.PENDING
            if preference["status"] == 201
            else ExternalProviderPaymentStatus.ERROR
        )

        self.logger.dict_to_table(preference["response"])
        await self.add_external_provider_request(
            request.end_to_end_id,
            preference["response"]["id"],
            request.model_dump(),
            preference,
        )

        if status == ExternalProviderPaymentStatus.ERROR:
            self.logger.error("Error creating order")
            raise DomainException("Error creating order")

        self.logger.info("Order successfully created")
        return ExternalOrderEntity(
            id=preference["response"]["id"],
            client_id=request.client_id,
            status=status,
            end_to_end_id=request.end_to_end_id,
            amount=total_amount,
            redirect_url=preference["response"]["sandbox_init_point"],
            provider=ExternalProvider.MERCADOPAGO,
            provider_result=preference,
        )

    async def cancel_order(self):
        return await super().cancel_order()

    async def refund_order(self):
        return await super().refund_order()

    async def get_order(self):
        return await super().get_order()

    async def process_external_feedback(
        self, notification: PaymentNotificationDataclass
    ) -> ExternalOrderPaymentResultModel:
        self.logger.title_box("Processing external feedback from Mercado Pago")
        payment = self.__sdk.payment().get(notification.data["id"])

        # self.logger.dict_to_table(payment["response"])

        return ExternalOrderPaymentResultModel(
            end_to_end_id=payment["response"]["external_reference"],
            status=(
                ExternalProviderPaymentStatus.APPROVED
                if payment["response"]["status"] == "approved"
                else ExternalProviderPaymentStatus.REJECTED
            ),
            provider=ExternalProvider.MERCADOPAGO,
        )
