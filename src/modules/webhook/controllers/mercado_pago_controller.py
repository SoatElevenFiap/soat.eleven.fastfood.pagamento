from http import HTTPMethod

from modules.shared.adapters import APIController
from modules.shared.decorators import API
from modules.shared.services.mercadopago.models import MercadoPagoNotificationModel
from modules.webhook.providers.process_mercado_pago_message_service_provider import (
    ProccessMercadoPagoMessageServiceProvider,
)


@API.controller("webhook/mercado-pago", "Mercado Pago")
class MercadoPagoWebhookController(APIController):
    @API.route("/", method=HTTPMethod.POST)
    async def mercado_pago_webhook(
        self,
        notification: MercadoPagoNotificationModel,
        proccess_mercado_pago_message_service: ProccessMercadoPagoMessageServiceProvider,
    ):
        await proccess_mercado_pago_message_service.process(notification)
        return {"message": "External feedback processed successfully"}
