from typing import Optional

from modules.client.constants import ClientCacheKeys
from modules.client.entities.client_entity import ClientEntity
from modules.client.repositories.client_repository import ClientRepository
from modules.shared.adapters import DomainService
from modules.shared.services.cache_manager import CacheManagerService
from modules.shared.services.cache_manager.config.ttl import TTL


class GetClientService(DomainService):
    def __init__(self, cache_manager_service: CacheManagerService, client_repository: ClientRepository):
        self.__client_repository = client_repository
        self.__cache_manager_service = cache_manager_service
        super().__init__(context=GetClientService.__name__)

    async def process(self, client_id: str) -> Optional[ClientEntity]:
        self.logger.info(f"Getting client: {client_id}")
        return await self.__cache_manager_service.build_cache_operation(
            key=ClientCacheKeys.client_key_for(client_id),
            callback=lambda: self.__client_repository.get_client(client_id),
            entity_class=ClientEntity,
        )
