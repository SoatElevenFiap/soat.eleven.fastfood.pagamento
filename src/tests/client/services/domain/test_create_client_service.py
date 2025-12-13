import pytest
from faker import Faker
from pytest_mock import MockFixture
from modules.client.constants import ClientCacheKeys
from modules.client.services.domain.create_client_service import CreateClientService
from modules.shared.services.cache_manager import CacheManagerService
from modules.client.repositories.client_repository import ClientRepository
from modules.client.services.domain.get_client_by_notification_url_service import GetClientByNotificationUrlService
from modules.client.services.domain.get_client_service import GetClientService
from modules.shared.exceptions.domain_exception import DomainException
from modules.shared.constants import ExceptionConstants
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestCreateClientService:
    @pytest.fixture
    def create_client_service(self, mocker: MockFixture) -> CreateClientService:
        self.faker = Faker()

        self.cache_manager_service = mocker.MagicMock(spec=CacheManagerService)
        self.cache_manager_service.set_value = mocker.Mock()
        self.cache_manager_service.expire_keys = mocker.Mock()

        self.get_client_by_notification_url_service = mocker.MagicMock(spec=GetClientByNotificationUrlService)
        self.get_client_by_notification_url_service.process = mocker.AsyncMock(return_value=None)

        self.client_repository = mocker.MagicMock(spec=ClientRepository)
        self.client_repository.add_client = mocker.AsyncMock()

        self.get_client_service = mocker.MagicMock(spec=GetClientService)
        self.get_client_service.process = mocker.AsyncMock()

        return CreateClientService(
            cache_manager_service=self.cache_manager_service,
            get_client_by_notification_url_service=self.get_client_by_notification_url_service,
            client_repository=self.client_repository,
            get_client_service=self.get_client_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_call_services_with_correct_params(
        self, create_client_service: CreateClientService
    ):
        fake_client = FakerClient.create()
        self.client_repository.add_client.return_value = fake_client

        sut = await create_client_service.process(fake_client.name, fake_client.notification_url)

        self.get_client_by_notification_url_service.process.assert_called_once_with(fake_client.notification_url)
        self.client_repository.add_client.assert_called_once()
        self.cache_manager_service.expire_keys.assert_called_once_with([ClientCacheKeys.ALL_CLIENTS_KEY])
        self.cache_manager_service.set_value.assert_called_once()
        call_args = self.cache_manager_service.set_value.call_args
        assert call_args[0][0] == ClientCacheKeys.client_key_for(fake_client.id)
        assert call_args[0][1] == fake_client.model_dump_json(), "Should pass serialized client JSON"
        assert sut == fake_client, "Client should be created"

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_raise_exception_when_client_already_exists(
        self, create_client_service: CreateClientService
    ):
        fake_client = FakerClient.create()
        self.get_client_by_notification_url_service.process.return_value = fake_client

        with pytest.raises(DomainException) as exc_info:
            await create_client_service.process(fake_client.name, fake_client.notification_url)

        assert exc_info.value.code == ExceptionConstants.CLIENT_ALREADY_EXISTS
        self.get_client_by_notification_url_service.process.assert_called_once_with(fake_client.notification_url)
        self.client_repository.add_client.assert_not_called()
        self.cache_manager_service.expire_keys.assert_not_called()
        self.cache_manager_service.set_value.assert_not_called()
