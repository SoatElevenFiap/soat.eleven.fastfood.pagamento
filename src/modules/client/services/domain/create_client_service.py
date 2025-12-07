import json
from typing import Optional
from modules.client.constants import ClientCacheKeys
from modules.client.entities.client_entity import ClientEntity
from modules.client.repositories.client_repository import ClientRepository
from modules.client.services.domain.get_client_service import GetClientService
from modules.shared.adapters import DomainService
from modules.shared.adapters.cache_adapter import CacheAdapter


class CreateClientService(DomainService):
    def __init__(self, cache: CacheAdapter, client_repository: ClientRepository, get_client_service: GetClientService):
        self.__client_repository = client_repository
        self.__cache = cache
        self.__get_client_service = get_client_service
        super().__init__(context=CreateClientService.__name__)

    async def process(self, name: str, notification_url: str) -> Optional[ClientEntity]:
        self.logger.info(f"Creating payment order...")
        entity = ClientEntity(
            name=name,
            notification_url=notification_url
        )
        client = await self.__client_repository.add_client(entity)
        self.logger.info(f"Client created: {client}")
        if client:
            self.__cache.set_value(ClientCacheKeys.client_key_for(client.id), client.model_dump_json())
            return client
        return None