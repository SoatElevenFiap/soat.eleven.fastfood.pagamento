
from http import HTTPMethod

from modules.shared.adapters import APIController
from modules.shared.decorators import API
from modules.shared.services.mercadopago.dataclasses import PaymentNotificationDataclass


@API.controller("webhook/mercado-pago")
class MercadoPagoWebhookController(APIController):
    @API.route("/", method=HTTPMethod.POST)
    async def mercado_pago_webhook(
        self,
        payment_notification: PaymentNotificationDataclass,
    ):
        return payment_notification