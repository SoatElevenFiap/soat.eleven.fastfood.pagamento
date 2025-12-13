import json
import pytest
from faker import Faker
from pytest_mock import MockFixture
from modules.client.constants import ClientCacheKeys
from modules.client.services.domain.get_client_service import GetClientService
from modules.shared.services.cache_manager import CacheManagerService
from modules.client.repositories.client_repository import ClientRepository
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestGetClientService:
    @pytest.fixture
    def get_client_service(self, mocker: MockFixture) -> GetClientService:
        self.faker = Faker()

        self.cache_manager_service = mocker.MagicMock(spec=CacheManagerService)
        self.cache_manager_service.build_cache_operation = mocker.AsyncMock()

        self.client_repository = mocker.MagicMock(spec=ClientRepository)
        self.client_repository.get_client = mocker.AsyncMock()

        return GetClientService(
            cache_manager_service=self.cache_manager_service,
            client_repository=self.client_repository,
        )

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_get_client_from_cache(
        self, get_client_service: GetClientService
    ):
        fake_client = FakerClient.create()
        self.cache_manager_service.build_cache_operation.return_value = fake_client

        sut = await get_client_service.process(fake_client.id)

        self.cache_manager_service.build_cache_operation.assert_called_once()
        call_args = self.cache_manager_service.build_cache_operation.call_args
        assert call_args.kwargs["key"] == ClientCacheKeys.client_key_for(fake_client.id)
        assert call_args.kwargs["entity_class"].__name__ == "ClientEntity"
        assert sut == fake_client, "Should return client from cache"

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_get_client_from_repository_when_not_in_cache(
        self, get_client_service: GetClientService
    ):
        fake_client = FakerClient.create()
        self.cache_manager_service.build_cache_operation.return_value = fake_client

        sut = await get_client_service.process(fake_client.id)

        self.cache_manager_service.build_cache_operation.assert_called_once()
        call_args = self.cache_manager_service.build_cache_operation.call_args
        assert call_args.kwargs["key"] == ClientCacheKeys.client_key_for(fake_client.id)
        assert call_args.kwargs["entity_class"].__name__ == "ClientEntity"
        assert sut == fake_client, "Should return client from repository"

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_return_none_when_client_not_found(
        self, get_client_service: GetClientService
    ):
        client_id = self.faker.uuid4()
        self.cache_manager_service.build_cache_operation.return_value = None

        sut = await get_client_service.process(client_id)

        self.cache_manager_service.build_cache_operation.assert_called_once()
        call_args = self.cache_manager_service.build_cache_operation.call_args
        assert call_args.kwargs["key"] == ClientCacheKeys.client_key_for(client_id)
        assert sut is None, "Should return None when client not found"
