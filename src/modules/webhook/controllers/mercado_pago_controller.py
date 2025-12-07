from http import HTTPMethod
from typing import Any, Dict

from modules.shared.adapters import APIController
from modules.shared.decorators import API
from modules.webhook.providers import ProccessMercadoPagoMessageServiceProvider


@API.controller("webhook/mercado-pago", "Mercado Pago")
class MercadoPagoWebhookController(APIController):
    @API.route("/", method=HTTPMethod.POST)
    async def mercado_pago_webhook(
        self,
        notification: Dict[str, Any],
        proccess_mercado_pago_message_service: ProccessMercadoPagoMessageServiceProvider,
    ):
        await proccess_mercado_pago_message_service.process(notification)
        return {"message": "External feedback processed successfully"}
