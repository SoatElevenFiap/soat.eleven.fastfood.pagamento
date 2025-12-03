from modules.external_provider.adapters import ExternalProviderAdapter
from modules.shared.services.logger.logger_service import LoggerService
from modules.shared.services.mercadopago.dataclasses import PaymentNotificationDataclass


class MercadoPagoService(ExternalProviderAdapter):
    def __init__(self):
        self.logger = LoggerService(context="MercadoPagoService")

    async def create_order(self):
        return await super().create_order()

    async def cancel_order(self):
        return await super().cancel_order()

    async def refund_order(self):
        return await super().refund_order()

    async def get_order(self):
        return await super().get_order()

    async def process_external_feedback(
        self, notification: PaymentNotificationDataclass
    ):
        self.logger.title_box(f"Received notification from Mercado Pago")
        self.logger.dict_to_table(notification.model_dump())
        return True
