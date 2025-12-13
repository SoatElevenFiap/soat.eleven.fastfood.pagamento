from typing import Annotated

from fastapi import Depends

from modules.client.providers.client_repository_provider import ClientRepositoryProvider
from modules.client.services.domain.get_client_service import GetClientService
from modules.shared.providers.cache_manager_service_provider import CacheManagerServiceProvider


def get_client_service_provider(
    cache_manager_service: CacheManagerServiceProvider, client_repository: ClientRepositoryProvider
):
    return GetClientService(cache_manager_service=cache_manager_service, client_repository=client_repository)


GetClientServiceProvider = Annotated[
    GetClientService, Depends(get_client_service_provider)
]
