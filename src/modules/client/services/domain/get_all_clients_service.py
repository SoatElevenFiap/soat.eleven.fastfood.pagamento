from typing import List

from modules.client.entities.client_entity import ClientEntity
from modules.client.repositories.client_repository import ClientRepository
from modules.shared.adapters import DomainService


class GetAllClientsService(DomainService):
    def __init__(self, client_repository: ClientRepository):
        self.__client_repository = client_repository
        super().__init__(context=GetAllClientsService.__name__)

    async def process(self) -> List[ClientEntity]:
        self.logger.info("Getting all clients...")
        clients = await self.__client_repository.get_all_clients()
        self.logger.info(f"Found {len(clients)} clients")
        return clients

