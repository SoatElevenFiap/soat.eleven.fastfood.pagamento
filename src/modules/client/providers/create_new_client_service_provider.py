from typing import Annotated

from fastapi import Depends

from modules.client.providers.create_client_service_provider import (
    CreateClientServiceProvider,
)
from modules.client.services.application.create_new_client_service import (
    CreateNewClientService,
)


def create_new_client_service_provider(
    create_client_service: CreateClientServiceProvider,
):
    return CreateNewClientService(
        create_client_service=create_client_service,
    )


CreateNewClientServiceProvider = Annotated[
    CreateNewClientService, Depends(create_new_client_service_provider)
]
