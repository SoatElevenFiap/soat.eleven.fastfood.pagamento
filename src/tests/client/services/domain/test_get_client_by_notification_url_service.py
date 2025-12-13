import pytest
from faker import Faker
from pytest_mock import MockFixture
from modules.client.services.domain.get_client_by_notification_url_service import (
    GetClientByNotificationUrlService,
)
from modules.client.repositories.client_repository import ClientRepository
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestGetClientByNotificationUrlService:
    @pytest.fixture
    def get_client_by_notification_url_service(
        self, mocker: MockFixture
    ) -> GetClientByNotificationUrlService:
        self.faker = Faker()

        self.client_repository = mocker.MagicMock(spec=ClientRepository)
        self.client_repository.get_client_by_notification_url = mocker.AsyncMock()

        return GetClientByNotificationUrlService(client_repository=self.client_repository)

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_get_client_by_notification_url_successfully(
        self, get_client_by_notification_url_service: GetClientByNotificationUrlService
    ):
        fake_client = FakerClient.create()
        notification_url = fake_client.notification_url
        self.client_repository.get_client_by_notification_url.return_value = fake_client

        sut = await get_client_by_notification_url_service.process(notification_url)

        self.client_repository.get_client_by_notification_url.assert_called_once_with(
            notification_url
        )
        assert sut == fake_client, "Should return client when found"
        assert sut.notification_url == notification_url, "Notification URL should match"

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.client
    async def test_return_none_when_client_not_found_by_notification_url(
        self, get_client_by_notification_url_service: GetClientByNotificationUrlService
    ):
        notification_url = self.faker.url()
        self.client_repository.get_client_by_notification_url.return_value = None

        sut = await get_client_by_notification_url_service.process(notification_url)

        self.client_repository.get_client_by_notification_url.assert_called_once_with(
            notification_url
        )
        assert sut is None, "Should return None when client not found"
