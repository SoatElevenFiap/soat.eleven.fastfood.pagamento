from http import HTTPMethod
from typing import List

from modules.client.dtos import CreateClientRequestDto
from modules.client.entities.client_entity import ClientEntity
from modules.client.providers.create_new_client_service_provider import (
    CreateNewClientServiceProvider,
)
from modules.client.providers.get_all_clients_service_provider import (
    GetAllClientsServiceProvider,
)
from modules.shared.adapters import APIController
from modules.shared.decorators import API


@API.controller("client", "Cliente")
class ClientController(APIController):
    @API.route("/", method=HTTPMethod.POST)
    async def create_client(
        self,
        request: CreateClientRequestDto,
        create_new_client_service: CreateNewClientServiceProvider,
    ):
        return await create_new_client_service.process(request)

    @API.route("/", method=HTTPMethod.GET, response_model=List[ClientEntity])
    async def get_clients(
        self,
        get_all_clients_service: GetAllClientsServiceProvider,
    ):
        return await get_all_clients_service.process()