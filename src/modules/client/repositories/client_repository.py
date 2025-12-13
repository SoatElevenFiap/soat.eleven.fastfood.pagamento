from typing import List, Optional

from modules.client.constants import ClientCacheKeys
from modules.client.entities.client_entity import ClientEntity
from modules.shared.adapters import RepositoryAdapter
from modules.shared.providers import MongoServiceProvider
from modules.shared.services.cache_manager import CacheManagerService


class ClientRepository(RepositoryAdapter):
    def __init__(
        self,
        mongo_service: MongoServiceProvider,
        cache_manager_service: CacheManagerService,
    ):
        self.__mongo_service = mongo_service
        self.__cache_manager_service = cache_manager_service
        super().__init__(table="clients")

    async def add_client(self, client: ClientEntity) -> ClientEntity:
        client.generate_created_at()
        client.generate_updated_at()
        client_id = await self.__mongo_service.add_document(
            self.table, client.model_dump(exclude=["id"])
        )
        created_client = await self.get_client(client_id)
        if created_client:
            # Invalidar cache de lista e atualizar cache do cliente
            self.__cache_manager_service.expire_keys([ClientCacheKeys.ALL_CLIENTS_KEY])
            self.__cache_manager_service.set_value(
                ClientCacheKeys.client_key_for(created_client.id),
                created_client,
            )
        return created_client

    async def get_client(self, client_id: str) -> Optional[ClientEntity]:
        return await self.__cache_manager_service.build_cache_operation(
            key=ClientCacheKeys.client_key_for(client_id),
            callback=lambda: self.__get_client_from_db(client_id),
            entity_class=ClientEntity,
        )

    async def get_client_by_notification_url(
        self, notification_url: str
    ) -> Optional[ClientEntity]:
        # Busca por notification_url não usa cache (não é uma chave comum)
        return await self.__get_client_by_notification_url_from_db(notification_url)

    async def get_all_clients(self) -> List[ClientEntity]:
        return await self.__cache_manager_service.build_cache_operation(
            key=ClientCacheKeys.ALL_CLIENTS_KEY,
            callback=self.__get_all_clients_from_db,
            entity_class=ClientEntity,
        )

    async def __get_client_from_db(self, client_id: str) -> Optional[ClientEntity]:
        client_document = await self.__mongo_service.get_document(
            self.table, {"id": client_id}
        )
        return ClientEntity(**client_document) if client_document else None

    async def __get_client_by_notification_url_from_db(
        self, notification_url: str
    ) -> Optional[ClientEntity]:
        client_document = await self.__mongo_service.get_document(
            self.table, {"notification_url": notification_url}
        )
        return ClientEntity(**client_document) if client_document else None

    async def __get_all_clients_from_db(self) -> List[ClientEntity]:
        client_documents = await self.__mongo_service.get_all_documents(self.table)
        return [ClientEntity(**doc) for doc in client_documents]
