from typing import Optional

from modules.client.entities.client_entity import ClientEntity
from modules.client.repositories.client_repository import ClientRepository
from modules.shared.adapters import DomainService


class GetClientService(DomainService):
    def __init__(self, client_repository: ClientRepository):
        self.__client_repository = client_repository
        super().__init__(context=GetClientService.__name__)

    async def process(self, client_id: str) -> Optional[ClientEntity]:
        self.logger.info(f"Getting client: {client_id}")
        return await self.__client_repository.get_client(client_id)
