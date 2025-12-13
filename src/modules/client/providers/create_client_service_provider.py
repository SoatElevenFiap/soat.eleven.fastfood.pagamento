from typing import Annotated

from fastapi import Depends

from modules.client.providers.client_repository_provider import ClientRepositoryProvider
from modules.client.providers.get_client_by_notification_url_service_provider import GetClientByNotificationUrlServiceProvider
from modules.client.services.domain.create_client_service import CreateClientService


def create_client_service_provider(
    get_client_by_notification_url_service: GetClientByNotificationUrlServiceProvider,
    client_repository: ClientRepositoryProvider,
):
    return CreateClientService(
        get_client_by_notification_url_service=get_client_by_notification_url_service,
        client_repository=client_repository,
    )


CreateClientServiceProvider = Annotated[
    CreateClientService, Depends(create_client_service_provider)
]
