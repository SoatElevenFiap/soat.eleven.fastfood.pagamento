from typing import List
from modules.client.dtos import ClientDto
from modules.client.services.domain.get_all_clients_service import GetAllClientsService
from modules.shared.adapters import ApplicationService

class GetAllClientsApplicationService(ApplicationService):
    def __init__(self, get_all_clients_service: GetAllClientsService):
        self.__get_all_clients_service = get_all_clients_service
        super().__init__(context=GetAllClientsApplicationService.__name__)

    async def process(self) -> List[ClientDto]:
        self.logger.info("Getting all clients...")
        clients = await self.__get_all_clients_service.process()
        return [ClientDto.from_client_entity(client) for client in clients]