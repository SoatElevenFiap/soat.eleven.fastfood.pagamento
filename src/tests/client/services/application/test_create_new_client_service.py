import pytest
from faker import Faker
from pytest_mock import MockFixture

from modules.client.dtos.create_client_request_dataclass import CreateClientRequestDto
from modules.client.services.application.create_new_client_service import (
    CreateNewClientService,
)
from modules.client.services.domain.create_client_service import CreateClientService
from tests.client.fakers import FakerClient


@pytest.mark.asyncio
class TestCreateNewClientService:
    @pytest.fixture
    def create_new_client_service(self, mocker: MockFixture) -> CreateNewClientService:
        self.faker = Faker()

        self.create_client_service = mocker.MagicMock(spec=CreateClientService)
        self.create_client_service.process = mocker.AsyncMock()

        return CreateNewClientService(
            create_client_service=self.create_client_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.application
    @pytest.mark.client
    async def test_create_new_client_successfully(
        self, create_new_client_service: CreateNewClientService
    ):
        fake_client = FakerClient.create()
        request = CreateClientRequestDto(
            name=fake_client.name, notification_url=fake_client.notification_url
        )
        self.create_client_service.process.return_value = fake_client

        sut = await create_new_client_service.process(request)

        self.create_client_service.process.assert_called_once_with(
            request.name, request.notification_url
        )
        assert sut == fake_client, "Should create and return new client"
