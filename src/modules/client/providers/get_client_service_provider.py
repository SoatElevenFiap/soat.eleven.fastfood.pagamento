from typing import Annotated

from fastapi import Depends

from modules.client.providers.client_repository_provider import ClientRepositoryProvider
from modules.client.services.domain.get_client_service import GetClientService
from modules.shared.providers import RedisServiceProvider


def get_client_service_provider(redis_service: RedisServiceProvider, client_repository: ClientRepositoryProvider):
    return GetClientService(
        cache=redis_service,
        client_repository=client_repository
    )


GetClientServiceProvider = Annotated[
    GetClientService, Depends(get_client_service_provider)
]
