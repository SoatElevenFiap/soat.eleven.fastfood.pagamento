from typing import Optional

from modules.client.dtos import CreateClientRequestDto, ClientDto
from modules.client.services.domain.create_client_service import CreateClientService
from modules.shared.adapters import ApplicationService


class CreateNewClientService(ApplicationService):
    def __init__(
        self,
        create_client_service: CreateClientService,
    ):
        self.__create_client_service = create_client_service
        super().__init__(context=CreateNewClientService.__name__)

    async def process(self, request: CreateClientRequestDto) -> Optional[ClientDto]:
        self.logger.info("Creating new client...")
        return await self.__create_client_service.process(
            request.name, request.notification_url
        )
