import pytest
from faker import Faker
from pytest_mock import MockFixture
from modules.client.constants import ClientCacheKeys
from modules.client.services.domain.create_client_service import CreateClientService
from modules.shared.adapters.cache_adapter import CacheAdapter
from modules.client.repositories.client_repository import ClientRepository
from modules.client.services.domain.get_client_service import GetClientService
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestCreateClientService:
    @pytest.fixture
    def create_client_service(self, mocker: MockFixture) -> CreateClientService:
        self.faker = Faker()

        self.cache = mocker.MagicMock(spec=CacheAdapter)
        self.cache.set_value = mocker.AsyncMock()

        self.client_repository = mocker.MagicMock(spec=ClientRepository)
        self.client_repository.add_client = mocker.AsyncMock()

        self.get_client_service = mocker.MagicMock(spec=GetClientService)
        self.get_client_service.process = mocker.AsyncMock()

        return CreateClientService(
            cache=self.cache,
            client_repository=self.client_repository,
            get_client_service=self.get_client_service,
        )

    @pytest.mark.asyncio
    async def test_call_services_with_correct_params(
        self, create_client_service: CreateClientService
    ):
        fake_client = FakerClient.create()
        self.client_repository.add_client.return_value = fake_client

        sut = await create_client_service.process(fake_client.name, fake_client.notification_url)

        self.cache.set_value.assert_called_once_with(ClientCacheKeys.client_key_for(fake_client.id), fake_client.model_dump_json())
        assert sut == fake_client, "Client should be created"
