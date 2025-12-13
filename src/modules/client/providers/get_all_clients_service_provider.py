from typing import Annotated

from fastapi import Depends

from modules.client.providers.client_repository_provider import (
    ClientRepositoryProvider,
)
from modules.client.services.domain.get_all_clients_service import (
    GetAllClientsService,
)
from modules.shared.providers.cache_manager_service_provider import CacheManagerServiceProvider


def get_all_clients_service_provider(
    cache_manager_service: CacheManagerServiceProvider,
    client_repository: ClientRepositoryProvider,
):
    return GetAllClientsService(cache_manager_service=cache_manager_service, client_repository=client_repository)


GetAllClientsServiceProvider = Annotated[
    GetAllClientsService, Depends(get_all_clients_service_provider)
]

