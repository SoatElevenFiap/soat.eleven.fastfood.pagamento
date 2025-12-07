from typing import Optional

from modules.client.entities.client_entity import ClientEntity
from modules.client.repositories.client_repository import ClientRepository
from modules.shared.adapters import DomainService


class GetClientByNotificationUrlService(DomainService):
    def __init__(self, client_repository: ClientRepository):
        self.__client_repository = client_repository
        super().__init__(context=GetClientByNotificationUrlService.__name__)

    async def process(self, notification_url: str) -> Optional[ClientEntity]:
        self.logger.info(f"Getting client by notification url: {notification_url}")
        client = await self.__client_repository.get_client_by_notification_url(
            notification_url
        )
        self.logger.info(f"Client found: {client}")
        return client
