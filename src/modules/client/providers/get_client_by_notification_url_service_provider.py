from typing import Annotated

from fastapi import Depends

from modules.client.providers.client_repository_provider import ClientRepositoryProvider
from modules.client.services.domain.get_client_by_notification_url_service import (
    GetClientByNotificationUrlService,
)


def get_client_by_notification_url_service_provider(
    client_repository: ClientRepositoryProvider,
):
    return GetClientByNotificationUrlService(client_repository=client_repository)


GetClientByNotificationUrlServiceProvider = Annotated[
    GetClientByNotificationUrlService,
    Depends(get_client_by_notification_url_service_provider),
]
