from http import HTTPMethod

from modules.shared.adapters import APIController
from modules.shared.decorators import API
from modules.shared.providers.mercado_pago_service_provider import (
    MercadoPagoServiceProvider,
)
from modules.shared.services.mercadopago.dataclasses import PaymentNotificationDataclass


@API.controller("webhook/mercado-pago")
class MercadoPagoWebhookController(APIController):
    @API.route("/", method=HTTPMethod.POST)
    async def mercado_pago_webhook(
        self,
        payment_notification: PaymentNotificationDataclass,
        mercado_pago_service: MercadoPagoServiceProvider,
    ):
        await mercado_pago_service.process_external_feedback(payment_notification)
        return {"message": "External feedback processed successfully"}
