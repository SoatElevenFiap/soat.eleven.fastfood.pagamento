from typing import Any, Dict

from modules.shared.adapters import ApplicationService
from modules.shared.providers.mercado_pago_service_provider import (
    MercadoPagoServiceProvider,
)
from modules.shared.services.mercadopago.dataclasses import PaymentNotificationDataclass
from modules.webhook.providers.process_external_payment_result_service_provider import (
    ProcessExternalPaymentResultServiceProvider,
)
from modules.webhook.providers.save_webhook_notification_provider import (
    SaveWebhookNotificationServiceProvider,
)


class ProccessMercadoPagoMessageService(ApplicationService):
    def __init__(
        self,
        mercado_pago_service: MercadoPagoServiceProvider,
        save_webhook_notification_service: SaveWebhookNotificationServiceProvider,
        process_external_payment_result_service: ProcessExternalPaymentResultServiceProvider,
    ):
        self.mercado_pago_service = mercado_pago_service
        self.save_webhook_notification_service = save_webhook_notification_service
        self.process_external_payment_result_service = (
            process_external_payment_result_service
        )
        super().__init__(context=ProccessMercadoPagoMessageService.__name__)

    async def process(self, notification: Dict[str, Any]):
        try:
            self.logger.info("Saving webhook notification...")
            await self.save_webhook_notification_service.process(notification)
        except Exception as e:
            self.logger.error(f"Error saving webhook notification: {e}")

        if not notification.get("type"):
            self.logger.warning(
                f"Notification type is not present: {notification}, skipping..."
            )
            return

        if "payment" not in str(notification["type"]):
            self.logger.warning(
                f"Notification type is not payment: {notification['type']}, skipping..."
            )
            return

        payment_notification = PaymentNotificationDataclass(**notification)
        result_status = await self.mercado_pago_service.process_external_feedback(
            payment_notification
        )
        await self.process_external_payment_result_service.process(result_status)
