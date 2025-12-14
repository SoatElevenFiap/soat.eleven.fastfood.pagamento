import pytest
from pytest_mock import MockFixture

from modules.payment.repositories.payment_repository import PaymentRepository
from modules.payment.services.domain.get_payment_by_end_to_end_id_service import (
    GetPaymentByEndToEndIdService,
)
from tests.payment.fakers import FakerPaymentEntity


@pytest.mark.asyncio
class TestGetPaymentByEndToEndIdService:
    @pytest.fixture
    def get_payment_by_end_to_end_id_service(
        self, mocker: MockFixture
    ) -> GetPaymentByEndToEndIdService:
        self.payment_repository = mocker.MagicMock(spec=PaymentRepository)
        self.payment_repository.get_payment_by_end_to_end_id = mocker.AsyncMock()

        return GetPaymentByEndToEndIdService(
            payment_repository=self.payment_repository
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_by_end_to_end_id_successfully(
        self, get_payment_by_end_to_end_id_service: GetPaymentByEndToEndIdService
    ):
        fake_payment = FakerPaymentEntity.create()
        self.payment_repository.get_payment_by_end_to_end_id.return_value = fake_payment

        result = await get_payment_by_end_to_end_id_service.process(
            fake_payment.end_to_end_id
        )

        self.payment_repository.get_payment_by_end_to_end_id.assert_called_once_with(
            fake_payment.end_to_end_id
        )
        assert result == fake_payment

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_return_none_when_payment_not_found(
        self, get_payment_by_end_to_end_id_service: GetPaymentByEndToEndIdService
    ):
        end_to_end_id = "non-existent-id"
        self.payment_repository.get_payment_by_end_to_end_id.return_value = None

        result = await get_payment_by_end_to_end_id_service.process(end_to_end_id)

        self.payment_repository.get_payment_by_end_to_end_id.assert_called_once_with(
            end_to_end_id
        )
        assert result is None

