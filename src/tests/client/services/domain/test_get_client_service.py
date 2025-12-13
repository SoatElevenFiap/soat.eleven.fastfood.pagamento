import pytest
from faker import Faker
from pytest_mock import MockFixture
from modules.client.services.domain.get_client_service import GetClientService
from modules.client.repositories.client_repository import ClientRepository
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestGetClientService:
    @pytest.fixture
    def get_client_service(self, mocker: MockFixture) -> GetClientService:
        self.faker = Faker()

        self.client_repository = mocker.MagicMock(spec=ClientRepository)
        self.client_repository.get_client = mocker.AsyncMock()

        return GetClientService(client_repository=self.client_repository)

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_get_client_successfully(
        self, get_client_service: GetClientService
    ):
        fake_client = FakerClient.create()
        self.client_repository.get_client.return_value = fake_client

        sut = await get_client_service.process(fake_client.id)

        self.client_repository.get_client.assert_called_once_with(fake_client.id)
        assert sut == fake_client, "Should return client from repository"

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_return_none_when_client_not_found(
        self, get_client_service: GetClientService
    ):
        client_id = self.faker.uuid4()
        self.client_repository.get_client.return_value = None

        sut = await get_client_service.process(client_id)

        self.client_repository.get_client.assert_called_once_with(client_id)
        assert sut is None, "Should return None when client not found"
