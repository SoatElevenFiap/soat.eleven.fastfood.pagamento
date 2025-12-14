from typing import Annotated

from fastapi import Depends

from modules.client.providers.get_all_clients_service_provider import (
    GetAllClientsServiceProvider,
)
from modules.client.services.application.get_all_clients_application_service import (
    GetAllClientsApplicationService,
)


def get_all_clients_application_service_provider(
    get_all_clients_service: GetAllClientsServiceProvider,
):
    return GetAllClientsApplicationService(
        get_all_clients_service=get_all_clients_service
    )


GetAllClientsApplicationServiceProvider = Annotated[
    GetAllClientsApplicationService,
    Depends(get_all_clients_application_service_provider),
]
