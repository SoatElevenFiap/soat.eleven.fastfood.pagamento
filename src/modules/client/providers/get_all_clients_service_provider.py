from typing import Annotated

from fastapi import Depends

from modules.client.providers.client_repository_provider import (
    ClientRepositoryProvider,
)
from modules.client.services.domain.get_all_clients_service import (
    GetAllClientsService,
)


def get_all_clients_service_provider(
    client_repository: ClientRepositoryProvider,
):
    return GetAllClientsService(client_repository=client_repository)


GetAllClientsServiceProvider = Annotated[
    GetAllClientsService, Depends(get_all_clients_service_provider)
]
