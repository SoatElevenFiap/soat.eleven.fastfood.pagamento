import pytest
from faker import Faker
from pytest_mock import MockFixture
from modules.client.services.domain.get_all_clients_service import GetAllClientsService
from modules.client.repositories.client_repository import ClientRepository
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestGetAllClientsService:
    @pytest.fixture
    def get_all_clients_service(self, mocker: MockFixture) -> GetAllClientsService:
        self.faker = Faker()

        self.client_repository = mocker.MagicMock(spec=ClientRepository)
        self.client_repository.get_all_clients = mocker.AsyncMock()

        return GetAllClientsService(client_repository=self.client_repository)

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_get_all_clients_successfully(
        self, get_all_clients_service: GetAllClientsService
    ):
        fake_clients = [FakerClient.create() for _ in range(3)]
        self.client_repository.get_all_clients.return_value = fake_clients

        sut = await get_all_clients_service.process()

        self.client_repository.get_all_clients.assert_called_once()
        assert len(sut) == 3, "Should return all clients"
        assert sut == fake_clients, "Should return the same clients from repository"

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_get_all_clients_when_empty(
        self, get_all_clients_service: GetAllClientsService
    ):
        self.client_repository.get_all_clients.return_value = []

        sut = await get_all_clients_service.process()

        self.client_repository.get_all_clients.assert_called_once()
        assert len(sut) == 0, "Should return empty list when no clients exist"
        assert sut == [], "Should return empty list"
