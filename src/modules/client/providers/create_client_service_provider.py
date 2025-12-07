from typing import Annotated

from fastapi import Depends

from modules.client.providers.client_repository_provider import ClientRepositoryProvider
from modules.client.providers.get_client_service_provider import GetClientServiceProvider
from modules.client.services.domain.create_client_service import CreateClientService

from modules.shared.providers import RedisServiceProvider


def create_client_service_provider(redis_service: RedisServiceProvider, client_repository: ClientRepositoryProvider, get_client_service: GetClientServiceProvider):
    return CreateClientService(
        cache=redis_service,
        client_repository=client_repository,
        get_client_service=get_client_service
    )


CreateClientServiceProvider = Annotated[
    CreateClientService, Depends(create_client_service_provider)
]
