from typing import Optional
from modules.client.dtos import CreateClientRequestDto
from modules.client.entities.client_entity import ClientEntity
from modules.client.services.domain.create_client_service import CreateClientService
from modules.client.services.domain.get_client_by_notification_url_service import GetClientByNotificationUrlService
from modules.shared.adapters import ApplicationService


class CreateNewClientService(ApplicationService):
    def __init__(self, get_client_by_notification_url_service: GetClientByNotificationUrlService, create_client_service: CreateClientService):
        self.__get_client_by_notification_url_service = get_client_by_notification_url_service
        self.__create_client_service = create_client_service
        super().__init__(context=CreateNewClientService.__name__)

    async def process(self, request: CreateClientRequestDto) -> Optional[ClientEntity]:
        client = await self.__get_client_by_notification_url_service.process(request.notification_url)
        if client:
            self.logger.warning(f"Client already exists with notification url: {request.notification_url}")
            return client
        self.logger.info(f"Creating new client...")
        return await self.__create_client_service.process(request.name, request.notification_url)