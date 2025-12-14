import pytest
from pytest_mock import MockFixture

from modules.payment.repositories.payment_repository import PaymentRepository
from modules.payment.services.domain.get_payment_service import GetPaymentService
from tests.payment.fakers import FakerPaymentEntity


@pytest.mark.asyncio
class TestGetPaymentService:
    @pytest.fixture
    def get_payment_service(self, mocker: MockFixture) -> GetPaymentService:
        self.payment_repository = mocker.MagicMock(spec=PaymentRepository)
        self.payment_repository.get_payment = mocker.AsyncMock()

        return GetPaymentService(payment_repository=self.payment_repository)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_successfully(
        self, get_payment_service: GetPaymentService
    ):
        fake_payment = FakerPaymentEntity.create()
        self.payment_repository.get_payment.return_value = fake_payment

        result = await get_payment_service.process(fake_payment.id)

        self.payment_repository.get_payment.assert_called_once_with(fake_payment.id)
        assert result == fake_payment

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_return_none_when_payment_not_found(
        self, get_payment_service: GetPaymentService
    ):
        payment_id = "non-existent-id"
        self.payment_repository.get_payment.return_value = None

        result = await get_payment_service.process(payment_id)

        self.payment_repository.get_payment.assert_called_once_with(payment_id)
        assert result is None
