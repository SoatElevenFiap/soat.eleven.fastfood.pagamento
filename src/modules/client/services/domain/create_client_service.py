from typing import Optional

from modules.client.entities.client_entity import ClientEntity
from modules.client.repositories.client_repository import ClientRepository
from modules.client.services.domain.get_client_by_notification_url_service import (
    GetClientByNotificationUrlService,
)
from modules.shared.adapters import DomainService
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException


class CreateClientService(DomainService):
    def __init__(
        self,
        get_client_by_notification_url_service: GetClientByNotificationUrlService,
        client_repository: ClientRepository,
    ):
        self.__client_repository = client_repository
        self.__get_client_by_notification_url_service = (
            get_client_by_notification_url_service
        )
        super().__init__(context=CreateClientService.__name__)

    async def process(self, name: str, notification_url: str) -> Optional[ClientEntity]:
        client = await self.__get_client_by_notification_url_service.process(
            notification_url
        )
        if client:
            self.logger.warning(
                f"Client already exists with notification url: {notification_url}"
            )
            raise DomainException(
                ExceptionConstants.CLIENT_ALREADY_EXISTS,
                f"Client already exists with notification url: {notification_url}",
            )
        self.logger.info("Creating client...")
        entity = ClientEntity(name=name, notification_url=notification_url)
        client = await self.__client_repository.add_client(entity)
        self.logger.info(f"Client created: {client}")
        return client
