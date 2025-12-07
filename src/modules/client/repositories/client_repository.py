from typing import List, Optional

from modules.client.entities.client_entity import ClientEntity
from modules.shared.adapters import RepositoryAdapter
from modules.shared.providers import MongoServiceProvider


class ClientRepository(RepositoryAdapter):
    def __init__(self, mongo_service: MongoServiceProvider):
        self.__mongo_service = mongo_service
        super().__init__(table="clients")

    async def add_client(self, client: ClientEntity) -> ClientEntity:
        client.generate_created_at()
        client.generate_updated_at()
        client_id = await self.__mongo_service.add_document(
            self.table, client.model_dump(exclude=["id"])
        )
        return await self.get_client(client_id)

    async def get_client(self, client_id: str) -> Optional[ClientEntity]:
        client_document = await self.__mongo_service.get_document(
            self.table, {"id": client_id}
        )
        return ClientEntity(**client_document) if client_document else None

    async def get_client_by_notification_url(
        self, notification_url: str
    ) -> Optional[ClientEntity]:
        client_document = await self.__mongo_service.get_document(
            self.table, {"notification_url": notification_url}
        )
        return ClientEntity(**client_document) if client_document else None

    async def get_all_clients(self) -> List[ClientEntity]:
        client_documents = await self.__mongo_service.get_all_documents(self.table)
        return [ClientEntity(**doc) for doc in client_documents]
