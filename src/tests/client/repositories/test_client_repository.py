import pytest
from pytest_mock import MockFixture

from modules.client.constants import ClientCacheKeys
from modules.client.entities.client_entity import ClientEntity
from modules.client.repositories.client_repository import ClientRepository
from modules.shared.providers.mongo_service_provider import MongoServiceProvider
from modules.shared.services.cache_manager import CacheManagerService
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestClientRepository:
    @pytest.fixture
    def client_repository(self, mocker: MockFixture) -> ClientRepository:
        self.mongo_service = mocker.MagicMock(spec=MongoServiceProvider)
        self.mongo_service.add_document = mocker.AsyncMock()
        self.mongo_service.get_document = mocker.AsyncMock()
        self.mongo_service.get_all_documents = mocker.AsyncMock()

        self.cache_manager_service = mocker.MagicMock(spec=CacheManagerService)
        self.cache_manager_service.build_cache_operation = mocker.AsyncMock()
        self.cache_manager_service.expire_keys = mocker.Mock()
        self.cache_manager_service.set_value = mocker.Mock()

        return ClientRepository(
            mongo_service=self.mongo_service,
            cache_manager_service=self.cache_manager_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_add_client_successfully(self, client_repository: ClientRepository):
        fake_client = FakerClient.create()
        client_id = "test-client-id"

        self.mongo_service.add_document.return_value = client_id
        self.cache_manager_service.build_cache_operation.return_value = fake_client

        result = await client_repository.add_client(fake_client)

        self.mongo_service.add_document.assert_called_once()
        call_args = self.mongo_service.add_document.call_args
        assert call_args[0][0] == "clients"
        assert "name" in call_args[0][1]
        assert "notification_url" in call_args[0][1]
        assert "created_at" in call_args[0][1]
        assert "updated_at" in call_args[0][1]
        assert "id" not in call_args[0][1]
        self.cache_manager_service.expire_keys.assert_called_once_with(
            [ClientCacheKeys.ALL_CLIENTS_KEY]
        )
        self.cache_manager_service.set_value.assert_called_once_with(
            ClientCacheKeys.client_key_for(fake_client.id), fake_client
        )
        assert result == fake_client

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_client_successfully(self, client_repository: ClientRepository):
        fake_client = FakerClient.create()
        client_id = fake_client.id

        self.cache_manager_service.build_cache_operation.return_value = fake_client

        result = await client_repository.get_client(client_id)

        self.cache_manager_service.build_cache_operation.assert_called_once()
        call_args = self.cache_manager_service.build_cache_operation.call_args
        assert call_args.kwargs["key"] == ClientCacheKeys.client_key_for(client_id)
        assert call_args.kwargs["entity_class"] == ClientEntity
        assert result == fake_client

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_client_returns_none_when_not_found(
        self, client_repository: ClientRepository
    ):
        client_id = "non-existent-id"

        self.cache_manager_service.build_cache_operation.return_value = None

        result = await client_repository.get_client(client_id)

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_client_by_notification_url_successfully(
        self, client_repository: ClientRepository
    ):
        fake_client = FakerClient.create()
        notification_url = fake_client.notification_url

        self.mongo_service.get_document.return_value = fake_client.model_dump()

        result = await client_repository.get_client_by_notification_url(
            notification_url
        )

        self.mongo_service.get_document.assert_called_once_with(
            "clients", {"notification_url": notification_url}
        )
        assert isinstance(result, ClientEntity)
        assert result.notification_url == notification_url

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_client_by_notification_url_returns_none_when_not_found(
        self, client_repository: ClientRepository
    ):
        notification_url = "https://non-existent-url.com"

        self.mongo_service.get_document.return_value = None

        result = await client_repository.get_client_by_notification_url(
            notification_url
        )

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_all_clients_successfully(
        self, client_repository: ClientRepository
    ):
        fake_clients = [FakerClient.create(), FakerClient.create()]

        self.cache_manager_service.build_cache_operation.return_value = fake_clients

        result = await client_repository.get_all_clients()

        self.cache_manager_service.build_cache_operation.assert_called_once()
        call_args = self.cache_manager_service.build_cache_operation.call_args
        assert call_args.kwargs["key"] == ClientCacheKeys.ALL_CLIENTS_KEY
        assert call_args.kwargs["entity_class"] == ClientEntity
        assert result == fake_clients

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_all_clients_returns_empty_list_when_no_clients(
        self, client_repository: ClientRepository
    ):
        self.cache_manager_service.build_cache_operation.return_value = []

        result = await client_repository.get_all_clients()

        assert result == []
