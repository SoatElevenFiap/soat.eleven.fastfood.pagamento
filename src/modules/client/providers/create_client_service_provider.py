from typing import Annotated

from fastapi import Depends

from modules.client.providers.client_repository_provider import ClientRepositoryProvider
from modules.client.providers.get_client_service_provider import (
    GetClientServiceProvider,
)
from modules.client.providers.get_client_by_notification_url_service_provider import GetClientByNotificationUrlServiceProvider
from modules.client.services.domain.create_client_service import CreateClientService
from modules.shared.providers.cache_manager_service_provider import CacheManagerServiceProvider


def create_client_service_provider(
    cache_manager_service: CacheManagerServiceProvider,
    get_client_by_notification_url_service: GetClientByNotificationUrlServiceProvider,
    client_repository: ClientRepositoryProvider,
    get_client_service: GetClientServiceProvider,
):
    return CreateClientService(
        cache_manager_service=cache_manager_service,
        get_client_by_notification_url_service=get_client_by_notification_url_service,
        client_repository=client_repository,
        get_client_service=get_client_service,
    )


CreateClientServiceProvider = Annotated[
    CreateClientService, Depends(create_client_service_provider)
]
