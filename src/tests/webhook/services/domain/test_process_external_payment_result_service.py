import pytest
from pytest_mock import MockFixture

from modules.payment.enums import PaymentStatus
from modules.payment.services.domain.change_payment_status_service import (
    ChangePaymentStatusService,
)
from modules.webhook.services.domain.process_external_payment_result_service import (
    ProcessExternalPaymentResultService,
)
from tests.external_provider.fakers import FakerExternalOrderPaymentResult


@pytest.mark.asyncio
class TestProcessExternalPaymentResultService:
    @pytest.fixture
    def process_external_payment_result_service(
        self, mocker: MockFixture
    ) -> ProcessExternalPaymentResultService:
        self.change_payment_status_service = mocker.MagicMock(
            spec=ChangePaymentStatusService
        )
        self.change_payment_status_service.process = mocker.AsyncMock()

        return ProcessExternalPaymentResultService(
            change_payment_status_service=self.change_payment_status_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_process_payment_result_successfully(
        self,
        process_external_payment_result_service: ProcessExternalPaymentResultService,
    ):
        result = FakerExternalOrderPaymentResult.create(status=PaymentStatus.PAID)

        await process_external_payment_result_service.process(result)

        self.change_payment_status_service.process.assert_called_once_with(
            result.end_to_end_id, PaymentStatus.PAID
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_process_payment_result_with_pending_status(
        self,
        process_external_payment_result_service: ProcessExternalPaymentResultService,
    ):
        result = FakerExternalOrderPaymentResult.create(status=PaymentStatus.PENDING)

        await process_external_payment_result_service.process(result)

        self.change_payment_status_service.process.assert_called_once_with(
            result.end_to_end_id, PaymentStatus.PENDING
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_process_payment_result_with_failed_status(
        self,
        process_external_payment_result_service: ProcessExternalPaymentResultService,
    ):
        result = FakerExternalOrderPaymentResult.create(status=PaymentStatus.FAILED)

        await process_external_payment_result_service.process(result)

        self.change_payment_status_service.process.assert_called_once_with(
            result.end_to_end_id, PaymentStatus.FAILED
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_process_payment_result_with_cancelled_status(
        self,
        process_external_payment_result_service: ProcessExternalPaymentResultService,
    ):
        result = FakerExternalOrderPaymentResult.create(status=PaymentStatus.CANCELLED)

        await process_external_payment_result_service.process(result)

        self.change_payment_status_service.process.assert_called_once_with(
            result.end_to_end_id, PaymentStatus.CANCELLED
        )
