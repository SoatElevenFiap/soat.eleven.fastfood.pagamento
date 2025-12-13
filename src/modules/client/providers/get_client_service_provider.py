from typing import Annotated

from fastapi import Depends

from modules.client.providers.client_repository_provider import ClientRepositoryProvider
from modules.client.services.domain.get_client_service import GetClientService


def get_client_service_provider(
    client_repository: ClientRepositoryProvider
):
    return GetClientService(client_repository=client_repository)


GetClientServiceProvider = Annotated[
    GetClientService, Depends(get_client_service_provider)
]
