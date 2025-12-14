import pytest
from pytest_mock import MockFixture

from modules.external_provider.repositories.external_provider_repository import (
    ExternalProviderRepository,
)
from modules.shared.providers.mongo_service_provider import MongoServiceProvider


@pytest.mark.asyncio
class TestExternalProviderRepository:
    @pytest.fixture
    def external_provider_repository(
        self, mocker: MockFixture
    ) -> ExternalProviderRepository:
        self.mongo_service = mocker.MagicMock(spec=MongoServiceProvider)
        self.mongo_service.add_document = mocker.AsyncMock()

        return ExternalProviderRepository(mongo_service=self.mongo_service)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_add_external_provider_request_successfully(
        self, external_provider_repository: ExternalProviderRepository
    ):
        request = {
            "provider": "mercadopago",
            "order_id": "test-order-id",
            "status": "pending",
            "data": {"key": "value"},
        }

        await external_provider_repository.add_external_provider_request(request)

        self.mongo_service.add_document.assert_called_once_with(
            "external_provider_requests", request
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_add_external_provider_request_with_empty_dict(
        self, external_provider_repository: ExternalProviderRepository
    ):
        request = {}

        await external_provider_repository.add_external_provider_request(request)

        self.mongo_service.add_document.assert_called_once_with(
            "external_provider_requests", request
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_add_external_provider_request_with_complex_data(
        self, external_provider_repository: ExternalProviderRepository
    ):
        request = {
            "provider": "mercadopago",
            "order_id": "test-order-id",
            "status": "pending",
            "data": {
                "payment_id": "123456",
                "amount": 100.50,
                "currency": "BRL",
                "metadata": {"key1": "value1", "key2": "value2"},
            },
        }

        await external_provider_repository.add_external_provider_request(request)

        self.mongo_service.add_document.assert_called_once_with(
            "external_provider_requests", request
        )
