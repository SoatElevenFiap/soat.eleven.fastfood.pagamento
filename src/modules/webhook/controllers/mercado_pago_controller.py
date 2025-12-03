from http import HTTPMethod

from modules.shared.adapters import APIController
from modules.shared.decorators import API
from modules.shared.services.mercadopago.dataclasses import PaymentNotificationDataclass
from modules.webhook.providers import ProccessMercadoPagoMessageServiceProvider


@API.controller("webhook/mercado-pago")
class MercadoPagoWebhookController(APIController):
    @API.route("/", method=HTTPMethod.POST)
    async def mercado_pago_webhook(
        self,
        payment_notification: PaymentNotificationDataclass,
        proccess_mercado_pago_message_service: ProccessMercadoPagoMessageServiceProvider,
    ):
        await proccess_mercado_pago_message_service.process(payment_notification)
        return {"message": "External feedback processed successfully"}
