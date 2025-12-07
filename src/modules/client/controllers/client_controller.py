from http import HTTPMethod

from modules.client.dtos import CreateClientRequestDto
from modules.client.providers.create_new_client_service_provider import (
    CreateNewClientServiceProvider,
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
