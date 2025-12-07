from typing import Annotated

from fastapi import Depends

from modules.client.providers.create_client_service_provider import CreateClientServiceProvider
from modules.client.providers.get_client_by_notification_url_service_provider import GetClientByNotificationUrlServiceProvider
from modules.client.services.application.create_new_client_service import CreateNewClientService


def create_new_client_service_provider(get_client_by_notification_url_service: GetClientByNotificationUrlServiceProvider, create_client_service: CreateClientServiceProvider):
    return CreateNewClientService(
        get_client_by_notification_url_service=get_client_by_notification_url_service,
        create_client_service=create_client_service
    )


CreateNewClientServiceProvider = Annotated[
    CreateNewClientService, Depends(create_new_client_service_provider)
]
