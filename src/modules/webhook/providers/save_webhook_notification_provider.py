from typing import Annotated

from fastapi import Depends

from modules.shared.providers.mongo_service_provider import MongoServiceProvider
from modules.webhook.services.domain.save_webhook_notification import SaveWebhookNotificationService


def save_webhook_notification_service_provider(mongo_service: MongoServiceProvider):
    return SaveWebhookNotificationService(
        mongo_service=mongo_service,
    )


SaveWebhookNotificationServiceProvider = Annotated[SaveWebhookNotificationService, Depends(save_webhook_notification_service_provider)]
