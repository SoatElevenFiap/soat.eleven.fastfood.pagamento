from typing import List

from modules.client.constants import ClientCacheKeys
from modules.client.entities.client_entity import ClientEntity
from modules.client.repositories.client_repository import ClientRepository
from modules.shared.adapters import DomainService
from modules.shared.services.cache_manager import CacheManagerService


class GetAllClientsService(DomainService):
    def __init__(self, cache_manager_service: CacheManagerService, client_repository: ClientRepository):
        self.__client_repository = client_repository
        self.__cache_manager_service = cache_manager_service
        super().__init__(context=GetAllClientsService.__name__)

    async def process(self) -> List[ClientEntity]:
        self.logger.info("Getting all clients...")
        return await self.__cache_manager_service.build_cache_operation(
            key=ClientCacheKeys.ALL_CLIENTS_KEY,
            callback=self.__client_repository.get_all_clients,
            entity_class=ClientEntity,
        )

