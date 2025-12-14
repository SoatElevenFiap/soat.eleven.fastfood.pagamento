import pytest
from pytest_mock import MockFixture

from modules.notification.services.domain.notify_listeners_service import (
    NotifyListenersService,
)
from modules.payment.enums import PaymentStatus
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.payment.services.domain.change_payment_status_service import (
    ChangePaymentStatusService,
)
from modules.payment.services.domain.get_payment_by_end_to_end_id_service import (
    GetPaymentByEndToEndIdService,
)
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException
from tests.payment.fakers import FakerPaymentEntity


@pytest.mark.asyncio
class TestChangePaymentStatusService:
    @pytest.fixture
    def change_payment_status_service(
        self, mocker: MockFixture
    ) -> ChangePaymentStatusService:
        self.notify_listeners_service = mocker.MagicMock(spec=NotifyListenersService)
        self.notify_listeners_service.process = mocker.AsyncMock()

        self.payment_repository = mocker.MagicMock(spec=PaymentRepository)
        self.payment_repository.change_payment_status = mocker.AsyncMock()

        self.get_payment_by_end_to_end_id_service = mocker.MagicMock(
            spec=GetPaymentByEndToEndIdService
        )
        self.get_payment_by_end_to_end_id_service.process = mocker.AsyncMock()

        return ChangePaymentStatusService(
            notify_listeners_service=self.notify_listeners_service,
            payment_repository=self.payment_repository,
            get_payment_by_end_to_end_id_service=self.get_payment_by_end_to_end_id_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_change_payment_status_successfully(
        self, change_payment_status_service: ChangePaymentStatusService
    ):
        fake_payment = FakerPaymentEntity.create(status=PaymentStatus.PENDING)
        updated_payment = FakerPaymentEntity.create(
            id=fake_payment.id, status=PaymentStatus.PAID
        )

        self.get_payment_by_end_to_end_id_service.process.return_value = fake_payment
        self.payment_repository.change_payment_status.return_value = updated_payment

        result = await change_payment_status_service.process(
            fake_payment.end_to_end_id, PaymentStatus.PAID
        )

        self.get_payment_by_end_to_end_id_service.process.assert_called_once_with(
            fake_payment.end_to_end_id
        )
        self.payment_repository.change_payment_status.assert_called_once_with(
            fake_payment.id, PaymentStatus.PAID
        )
        self.notify_listeners_service.process.assert_called_once_with(fake_payment)
        assert result == updated_payment

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_raise_exception_when_payment_not_found(
        self, change_payment_status_service: ChangePaymentStatusService
    ):
        end_to_end_id = "non-existent-id"
        self.get_payment_by_end_to_end_id_service.process.return_value = None

        with pytest.raises(DomainException) as exc_info:
            await change_payment_status_service.process(
                end_to_end_id, PaymentStatus.PAID
            )

        assert exc_info.value.code == ExceptionConstants.PAYMENT_NOT_FOUND
        assert end_to_end_id in exc_info.value.message
        self.get_payment_by_end_to_end_id_service.process.assert_called_once_with(
            end_to_end_id
        )
        self.payment_repository.change_payment_status.assert_not_called()
        self.notify_listeners_service.process.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_not_notify_when_payment_update_fails(
        self, change_payment_status_service: ChangePaymentStatusService
    ):
        fake_payment = FakerPaymentEntity.create()
        self.get_payment_by_end_to_end_id_service.process.return_value = fake_payment
        self.payment_repository.change_payment_status.return_value = None

        result = await change_payment_status_service.process(
            fake_payment.end_to_end_id, PaymentStatus.PAID
        )

        self.get_payment_by_end_to_end_id_service.process.assert_called_once()
        self.payment_repository.change_payment_status.assert_called_once()
        self.notify_listeners_service.process.assert_not_called()
        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_change_status_to_failed(
        self, change_payment_status_service: ChangePaymentStatusService
    ):
        fake_payment = FakerPaymentEntity.create(status=PaymentStatus.PENDING)
        updated_payment = FakerPaymentEntity.create(
            id=fake_payment.id, status=PaymentStatus.FAILED
        )

        self.get_payment_by_end_to_end_id_service.process.return_value = fake_payment
        self.payment_repository.change_payment_status.return_value = updated_payment

        result = await change_payment_status_service.process(
            fake_payment.end_to_end_id, PaymentStatus.FAILED
        )

        self.payment_repository.change_payment_status.assert_called_once_with(
            fake_payment.id, PaymentStatus.FAILED
        )
        self.notify_listeners_service.process.assert_called_once()
        assert result == updated_payment
