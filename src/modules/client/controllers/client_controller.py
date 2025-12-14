from http import HTTPMethod
from typing import List

from modules.client.dtos import ClientDto, CreateClientRequestDto
from modules.client.providers.create_new_client_service_provider import (
    CreateNewClientServiceProvider,
)
from modules.client.providers.get_all_clients_application_service_provider import (
    GetAllClientsApplicationServiceProvider,
)
from modules.shared.adapters import APIController
from modules.shared.decorators import API


@API.controller("client", "Cliente")
class ClientController(APIController):
    @API.route("/", method=HTTPMethod.POST, response_model=ClientDto)
    async def create_client(
        self,
        request: CreateClientRequestDto,
        create_new_client_service: CreateNewClientServiceProvider,
    ):
        return await create_new_client_service.process(request)

    @API.route("/", method=HTTPMethod.GET, response_model=List[ClientDto])
    async def get_clients(
        self,
        get_all_clients_application_service: GetAllClientsApplicationServiceProvider,
    ):
        return await get_all_clients_application_service.process()
