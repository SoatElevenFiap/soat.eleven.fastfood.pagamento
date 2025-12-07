from datetime import UTC, datetime

from modules.external_provider.enums import ExternalProvider
from modules.shared.adapters import DomainService
from modules.shared.services.mongo.mongo_service import MongoService


class SaveWebhookNotificationService(DomainService):
    def __init__(
        self,
        mongo_service: MongoService,
    ):
        self.mongo_service = mongo_service
        super().__init__(context=SaveWebhookNotificationService.__name__)

    async def process(self, notification: dict | str | list):
        await self.mongo_service.add_document(
            "notifications",
            {
                "notification": notification,
                "provider": ExternalProvider.MERCADOPAGO,
                "created_at": datetime.now(UTC),
            },
        )
