from modules.shared.providers.mercado_pago_service_provider import MercadoPagoServiceProvider
from modules.shared.services.mercadopago.dataclasses import PaymentNotificationDataclass
from modules.shared.adapters import ApplicationService
from modules.webhook.providers.save_webhook_notification_provider import SaveWebhookNotificationServiceProvider

class ProccessMercadoPagoMessageService(ApplicationService):
    def __init__(self, 
        mercado_pago_service: MercadoPagoServiceProvider,
        save_webhook_notification_service: SaveWebhookNotificationServiceProvider
    ):
        self.mercado_pago_service = mercado_pago_service
        self.save_webhook_notification_service = save_webhook_notification_service
        super().__init__(context=ProccessMercadoPagoMessageService.__name__)

    async def process(self, notification: PaymentNotificationDataclass):
        await self.mercado_pago_service.process_external_feedback(notification)
        try:
            self.logger.info(f"Saving webhook notification...")
            await self.save_webhook_notification_service.process(notification.model_dump())
        except Exception as e:
            self.logger.error(f"Error saving webhook notification: {e}")
        self.logger.info(f"Mercado Pago message processed successfully")
