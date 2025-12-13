import pytest
from faker import Faker
from pytest_mock import MockFixture
from modules.client.dtos import ClientDto
from modules.client.services.application.get_all_clients_application_service import (
    GetAllClientsApplicationService,
)
from modules.client.services.domain.get_all_clients_service import GetAllClientsService
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestGetAllClientsApplicationService:
    @pytest.fixture
    def get_all_clients_application_service(
        self, mocker: MockFixture
    ) -> GetAllClientsApplicationService:
        self.faker = Faker()

        self.get_all_clients_service = mocker.MagicMock(spec=GetAllClientsService)
        self.get_all_clients_service.process = mocker.AsyncMock()

        return GetAllClientsApplicationService(
            get_all_clients_service=self.get_all_clients_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.application
    @pytest.mark.client
    async def test_get_all_clients_successfully(
        self, get_all_clients_application_service: GetAllClientsApplicationService
    ):
        fake_clients = [FakerClient.create() for _ in range(3)]
        self.get_all_clients_service.process.return_value = fake_clients

        sut = await get_all_clients_application_service.process()

        self.get_all_clients_service.process.assert_called_once()
        assert len(sut) == 3, "Should return all clients as DTOs"
        assert all(isinstance(client, ClientDto) for client in sut), "All items should be ClientDto"
        assert sut[0].id == fake_clients[0].id, "First client ID should match"
        assert sut[0].name == fake_clients[0].name, "First client name should match"
        assert sut[0].notification_url == fake_clients[0].notification_url, "First client notification_url should match"

    @pytest.mark.asyncio
    @pytest.mark.application
    @pytest.mark.client
    async def test_get_all_clients_when_empty(
        self, get_all_clients_application_service: GetAllClientsApplicationService
    ):
        self.get_all_clients_service.process.return_value = []

        sut = await get_all_clients_application_service.process()

        self.get_all_clients_service.process.assert_called_once()
        assert len(sut) == 0, "Should return empty list when no clients exist"
        assert sut == [], "Should return empty list"
