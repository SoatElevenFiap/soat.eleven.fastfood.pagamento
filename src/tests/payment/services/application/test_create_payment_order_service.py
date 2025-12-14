import pytest
from pytest_mock import MockFixture

from modules.client.providers.get_client_service_provider import (
    GetClientServiceProvider,
)
from modules.external_provider.adapters.external_provider_adapter import (
    ExternalProviderAdapter,
)
from modules.external_provider.providers.get_external_provider_service_provider import (
    GetExternalProviderServiceProvider,
)
from modules.payment.dtos import CreatePaymentOrderRequestDto
from modules.payment.models.payment_item_model import PaymentItemModel
from modules.payment.providers.create_payment_service import (
    CreatePaymentServiceProvider,
)
from modules.payment.services.application.create_payment_order_service import (
    CreatePaymentOrderService,
)
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException
from tests.client.fakers import FakerClient
from tests.external_provider.fakers import FakerExternalOrderEntity
from tests.payment.fakers import FakerPaymentEntity


@pytest.mark.asyncio
class TestCreatePaymentOrderService:
    @pytest.fixture
    def create_payment_order_service(
        self, mocker: MockFixture
    ) -> CreatePaymentOrderService:
        self.get_client_service = mocker.MagicMock(spec=GetClientServiceProvider)
        self.get_client_service.process = mocker.AsyncMock()

        self.get_external_provider_service = mocker.MagicMock(
            spec=GetExternalProviderServiceProvider
        )
        self.get_external_provider_service.process = mocker.AsyncMock()

        self.create_payment_service = mocker.MagicMock(
            spec=CreatePaymentServiceProvider
        )
        self.create_payment_service.process = mocker.AsyncMock()

        return CreatePaymentOrderService(
            get_client_service=self.get_client_service,
            get_external_provider_service=self.get_external_provider_service,
            create_payment_service=self.create_payment_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_payment_order_successfully(
        self,
        create_payment_order_service: CreatePaymentOrderService,
        mocker: MockFixture,
    ):
        from faker import Faker

        faker = Faker()
        fake_client = FakerClient.create()
        fake_order = FakerExternalOrderEntity.create(client_id=fake_client.id)
        fake_payment = FakerPaymentEntity.create(
            id=faker.uuid4(),
            client_id=fake_order.client_id,
            end_to_end_id=fake_order.end_to_end_id,
        )

        request = CreatePaymentOrderRequestDto(
            client_id=fake_client.id,
            end_to_end_id=fake_order.end_to_end_id,
            items=[
                PaymentItemModel(title="Item 1", quantity=1, unit_price=10.0),
            ],
        )

        mock_external_provider = mocker.MagicMock(spec=ExternalProviderAdapter)
        mock_external_provider.create_order = mocker.AsyncMock(return_value=fake_order)

        self.get_client_service.process.return_value = fake_client
        self.get_external_provider_service.process.return_value = mock_external_provider
        self.create_payment_service.process.return_value = fake_payment

        result = await create_payment_order_service.process(request)

        self.get_client_service.process.assert_called_once_with(request.client_id)
        self.get_external_provider_service.process.assert_called_once()
        mock_external_provider.create_order.assert_called_once()
        self.create_payment_service.process.assert_called_once_with(fake_order)
        assert result.id == fake_payment.id

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_raise_exception_when_client_not_found(
        self, create_payment_order_service: CreatePaymentOrderService
    ):
        request = CreatePaymentOrderRequestDto(
            client_id="non-existent-id",
            end_to_end_id="e2e-123",
            items=[PaymentItemModel(title="Item 1", quantity=1, unit_price=10.0)],
        )

        self.get_client_service.process.return_value = None

        with pytest.raises(DomainException) as exc_info:
            await create_payment_order_service.process(request)

        assert exc_info.value.code == ExceptionConstants.CLIENT_NOT_FOUND
        assert request.client_id in exc_info.value.message
        self.get_client_service.process.assert_called_once_with(request.client_id)
        self.get_external_provider_service.process.assert_not_called()
        self.create_payment_service.process.assert_not_called()
