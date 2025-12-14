from modules.shared.adapters import ApplicationService
from modules.shared.providers.mercado_pago_service_provider import (
    MercadoPagoServiceProvider,
)
from modules.shared.services.mercadopago.models import MercadoPagoNotificationModel
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

    async def process(self, notification: MercadoPagoNotificationModel):
        try:
            self.logger.info("Saving webhook notification...")
            await self.save_webhook_notification_service.process(notification.to_dict())
        except Exception as e:
            self.logger.error(f"Error saving webhook notification: {e}")

        if not notification.has_type():
            self.logger.warning(
                f"Notification type is not present: {notification.to_dict()}, skipping..."
            )
            return

        if not notification.is_payment_notification():
            self.logger.warning(
                f"Notification type is not payment: {notification.type}, skipping..."
            )
            return

        result_status = await self.mercado_pago_service.process_external_feedback(
            notification
        )
        await self.process_external_payment_result_service.process(result_status)
