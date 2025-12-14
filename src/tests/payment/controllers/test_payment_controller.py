import pytest
from pytest_mock import MockFixture

from modules.payment.controllers.payment_controller import PaymentController
from modules.payment.dtos import CreatePaymentOrderRequestDto
from modules.payment.dtos.payment_dto import PaymentDto
from modules.payment.models.payment_item_model import PaymentItemModel
from modules.payment.providers import GetPaymentApplicationServiceProvider
from modules.payment.providers.create_payment_order_service import (
    CreatePaymentOrderServiceProvider,
)
from tests.payment.fakers import FakerPaymentEntity


@pytest.mark.asyncio
class TestPaymentController:
    @pytest.fixture
    def payment_controller(self) -> PaymentController:
        return PaymentController()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_payment_successfully(
        self, payment_controller: PaymentController, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create(id="test-payment-id")
        payment_dto = PaymentDto.from_payment_entity(fake_payment)
        request = CreatePaymentOrderRequestDto(
            client_id=fake_payment.client_id,
            end_to_end_id=fake_payment.end_to_end_id,
            items=[PaymentItemModel(title="Item 1", quantity=1, unit_price=10.0)],
        )

        mock_service = mocker.MagicMock(spec=CreatePaymentOrderServiceProvider)
        mock_service.process = mocker.AsyncMock(return_value=payment_dto)

        result = await payment_controller.create_payment(request, mock_service)

        mock_service.process.assert_called_once_with(request)
        assert result == payment_dto
        assert result.id == fake_payment.id
        assert result.client_id == fake_payment.client_id

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_by_id_successfully(
        self, payment_controller: PaymentController, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create(id="test-payment-id")
        payment_dto = PaymentDto.from_payment_entity(fake_payment)

        mock_service = mocker.MagicMock(spec=GetPaymentApplicationServiceProvider)
        mock_service.process = mocker.AsyncMock(return_value=payment_dto)

        result = await payment_controller.get_payment(
            mock_service, id=fake_payment.id, end_to_end_id=None
        )

        mock_service.process.assert_called_once_with(
            id=fake_payment.id, end_to_end_id=None
        )
        assert result == payment_dto
        assert result.id == fake_payment.id

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_by_end_to_end_id_successfully(
        self, payment_controller: PaymentController, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create(id="test-payment-id")
        payment_dto = PaymentDto.from_payment_entity(fake_payment)

        mock_service = mocker.MagicMock(spec=GetPaymentApplicationServiceProvider)
        mock_service.process = mocker.AsyncMock(return_value=payment_dto)

        result = await payment_controller.get_payment(
            mock_service, id=None, end_to_end_id=fake_payment.end_to_end_id
        )

        mock_service.process.assert_called_once_with(
            id=None, end_to_end_id=fake_payment.end_to_end_id
        )
        assert result == payment_dto
        assert result.end_to_end_id == fake_payment.end_to_end_id

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_with_both_parameters(
        self, payment_controller: PaymentController, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create(id="test-payment-id")
        payment_dto = PaymentDto.from_payment_entity(fake_payment)

        mock_service = mocker.MagicMock(spec=GetPaymentApplicationServiceProvider)
        mock_service.process = mocker.AsyncMock(return_value=payment_dto)

        result = await payment_controller.get_payment(
            mock_service, id=fake_payment.id, end_to_end_id=fake_payment.end_to_end_id
        )

        mock_service.process.assert_called_once_with(
            id=fake_payment.id, end_to_end_id=fake_payment.end_to_end_id
        )
        assert result == payment_dto

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_with_no_parameters(
        self, payment_controller: PaymentController, mocker: MockFixture
    ):
        mock_service = mocker.MagicMock(spec=GetPaymentApplicationServiceProvider)
        mock_service.process = mocker.AsyncMock(return_value=None)

        result = await payment_controller.get_payment(
            mock_service, id=None, end_to_end_id=None
        )

        mock_service.process.assert_called_once_with(id=None, end_to_end_id=None)
        assert result is None
