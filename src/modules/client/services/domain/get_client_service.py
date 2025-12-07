import json
from typing import Optional

from modules.client.constants import ClientCacheKeys
from modules.client.entities.client_entity import ClientEntity
from modules.client.repositories.client_repository import ClientRepository
from modules.shared.adapters import DomainService
from modules.shared.adapters.cache_adapter import CacheAdapter


class GetClientService(DomainService):
    def __init__(self, cache: CacheAdapter, client_repository: ClientRepository):
        self.__client_repository = client_repository
        self.__cache = cache
        super().__init__(context=GetClientService.__name__)

    async def process(self, client_id: str) -> Optional[ClientEntity]:
        self.logger.info(f"Getting client: {client_id}")
        cached_data = self.__cache.get_value(ClientCacheKeys.client_key_for(client_id))
        if cached_data:
            return ClientEntity(**json.loads(cached_data))
        client = await self.__client_repository.get_client(client_id)
        if client:
            self.__cache.set_value(
                ClientCacheKeys.client_key_for(client_id), client.model_dump_json()
            )
            return client
        return None
