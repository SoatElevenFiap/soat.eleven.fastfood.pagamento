from typing import Annotated

from fastapi import Depends

from modules.shared.providers.mercado_pago_service_provider import (
    MercadoPagoServiceProvider,
)
from modules.webhook.providers.process_external_payment_result_service_provider import (
    ProcessExternalPaymentResultServiceProvider,
)
from modules.webhook.providers.save_webhook_notification_provider import (
    SaveWebhookNotificationServiceProvider,
)
from modules.webhook.services.application.proccess_mercado_pago_message_service import (
    ProccessMercadoPagoMessageService,
)


def process_mercado_pago_message_service_provider(
    save_webhook_notification_service: SaveWebhookNotificationServiceProvider,
    mercado_pago_service: MercadoPagoServiceProvider,
    process_external_payment_result_service: ProcessExternalPaymentResultServiceProvider,
):
    return ProccessMercadoPagoMessageService(
        mercado_pago_service=mercado_pago_service,
        save_webhook_notification_service=save_webhook_notification_service,
        process_external_payment_result_service=process_external_payment_result_service,
    )


ProccessMercadoPagoMessageServiceProvider = Annotated[
    ProccessMercadoPagoMessageService,
    Depends(process_mercado_pago_message_service_provider),
]
