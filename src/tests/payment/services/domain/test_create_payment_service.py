import pytest
from pytest_mock import MockFixture

from modules.payment.repositories.payment_repository import PaymentRepository
from modules.payment.services.domain.create_payment_service import CreatePaymentService
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException
from tests.external_provider.fakers import FakerExternalOrderEntity
from tests.payment.fakers import FakerPaymentEntity


@pytest.mark.asyncio
class TestCreatePaymentService:
    @pytest.fixture
    def create_payment_service(self, mocker: MockFixture) -> CreatePaymentService:
        self.payment_repository = mocker.MagicMock(spec=PaymentRepository)
        self.payment_repository.get_payment_by_end_to_end_id = mocker.AsyncMock(
            return_value=None
        )
        self.payment_repository.add_payment = mocker.AsyncMock()

        return CreatePaymentService(payment_repository=self.payment_repository)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_payment_successfully(
        self, create_payment_service: CreatePaymentService
    ):
        fake_order = FakerExternalOrderEntity.create()
        fake_payment = FakerPaymentEntity.create(
            client_id=fake_order.client_id,
            end_to_end_id=fake_order.end_to_end_id,
            external_reference_id=fake_order.id,
            value=fake_order.amount,
            provider=fake_order.provider,
            redirect_url=fake_order.redirect_url,
        )

        self.payment_repository.add_payment.return_value = fake_payment

        result = await create_payment_service.process(fake_order)

        self.payment_repository.get_payment_by_end_to_end_id.assert_called_once_with(
            fake_order.end_to_end_id
        )
        self.payment_repository.add_payment.assert_called_once()
        assert result == fake_payment
        assert result.status.value == "pending"

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_raise_exception_when_payment_already_exists(
        self, create_payment_service: CreatePaymentService
    ):
        fake_order = FakerExternalOrderEntity.create()
        existing_payment = FakerPaymentEntity.create(
            end_to_end_id=fake_order.end_to_end_id
        )

        self.payment_repository.get_payment_by_end_to_end_id.return_value = (
            existing_payment
        )

        with pytest.raises(DomainException) as exc_info:
            await create_payment_service.process(fake_order)

        assert exc_info.value.code == ExceptionConstants.PAYMENT_ALREADY_EXISTS
        assert fake_order.end_to_end_id in exc_info.value.message
        self.payment_repository.get_payment_by_end_to_end_id.assert_called_once_with(
            fake_order.end_to_end_id
        )
        self.payment_repository.add_payment.assert_not_called()
