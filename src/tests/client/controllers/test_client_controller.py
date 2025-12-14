import pytest
from pytest_mock import MockFixture

from modules.client.controllers.client_controller import ClientController
from modules.client.dtos import ClientDto, CreateClientRequestDto
from modules.client.providers.create_new_client_service_provider import (
    CreateNewClientServiceProvider,
)
from modules.client.providers.get_all_clients_application_service_provider import (
    GetAllClientsApplicationServiceProvider,
)
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestClientController:
    @pytest.fixture
    def client_controller(self) -> ClientController:
        return ClientController()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_client_successfully(
        self, client_controller: ClientController, mocker: MockFixture
    ):
        fake_client = FakerClient.create()
        client_dto = ClientDto.from_client_entity(fake_client)
        request = CreateClientRequestDto(
            name=fake_client.name, notification_url=fake_client.notification_url
        )

        mock_service = mocker.MagicMock(spec=CreateNewClientServiceProvider)
        mock_service.process = mocker.AsyncMock(return_value=client_dto)

        result = await client_controller.create_client(request, mock_service)

        mock_service.process.assert_called_once_with(request)
        assert result == client_dto
        assert result.id == fake_client.id
        assert result.name == fake_client.name
        assert result.notification_url == fake_client.notification_url

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_clients_successfully(
        self, client_controller: ClientController, mocker: MockFixture
    ):
        fake_clients = [FakerClient.create(), FakerClient.create()]
        clients_dto = [ClientDto.from_client_entity(client) for client in fake_clients]

        mock_service = mocker.MagicMock(spec=GetAllClientsApplicationServiceProvider)
        mock_service.process = mocker.AsyncMock(return_value=clients_dto)

        result = await client_controller.get_clients(mock_service)

        mock_service.process.assert_called_once()
        assert result == clients_dto
        assert len(result) == 2

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_clients_returns_empty_list(
        self, client_controller: ClientController, mocker: MockFixture
    ):
        mock_service = mocker.MagicMock(spec=GetAllClientsApplicationServiceProvider)
        mock_service.process = mocker.AsyncMock(return_value=[])

        result = await client_controller.get_clients(mock_service)

        mock_service.process.assert_called_once()
        assert result == []
        assert len(result) == 0
