import pytest
from pytest_mock import MockFixture

from modules.payment.enums import PaymentStatus
from modules.shared.services.mercadopago.mercado_pago_service import (
    MercadoPagoService,
)
from modules.shared.services.mercadopago.models import MercadoPagoNotificationModel
from modules.webhook.services.application.proccess_mercado_pago_message_service import (
    ProccessMercadoPagoMessageService,
)
from modules.webhook.services.domain.process_external_payment_result_service import (
    ProcessExternalPaymentResultService,
)
from modules.webhook.services.domain.save_webhook_notification import (
    SaveWebhookNotificationService,
)
from tests.external_provider.fakers import FakerExternalOrderPaymentResult
from tests.webhook.fakers import FakerPaymentNotification


@pytest.mark.asyncio
class TestProccessMercadoPagoMessageService:
    @pytest.fixture
    def proccess_mercado_pago_message_service(
        self, mocker: MockFixture
    ) -> ProccessMercadoPagoMessageService:
        self.mercado_pago_service = mocker.MagicMock(spec=MercadoPagoService)
        self.mercado_pago_service.process_external_feedback = mocker.AsyncMock()

        self.save_webhook_notification_service = mocker.MagicMock(
            spec=SaveWebhookNotificationService
        )
        self.save_webhook_notification_service.process = mocker.AsyncMock()

        self.process_external_payment_result_service = mocker.MagicMock(
            spec=ProcessExternalPaymentResultService
        )
        self.process_external_payment_result_service.process = mocker.AsyncMock()

        return ProccessMercadoPagoMessageService(
            mercado_pago_service=self.mercado_pago_service,
            save_webhook_notification_service=self.save_webhook_notification_service,
            process_external_payment_result_service=self.process_external_payment_result_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_process_payment_notification_successfully(
        self, proccess_mercado_pago_message_service: ProccessMercadoPagoMessageService
    ):
        notification = FakerPaymentNotification.create()

        result_status = FakerExternalOrderPaymentResult.create(
            status=PaymentStatus.PAID
        )
        self.mercado_pago_service.process_external_feedback.return_value = result_status

        await proccess_mercado_pago_message_service.process(notification)

        self.save_webhook_notification_service.process.assert_called_once_with(
            notification.to_dict()
        )
        self.mercado_pago_service.process_external_feedback.assert_called_once()
        call_args = self.mercado_pago_service.process_external_feedback.call_args[0][0]
        assert isinstance(call_args, MercadoPagoNotificationModel)
        assert call_args.type == "payment"
        self.process_external_payment_result_service.process.assert_called_once_with(
            result_status
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_save_notification_even_when_processing_fails(
        self, proccess_mercado_pago_message_service: ProccessMercadoPagoMessageService
    ):
        notification = FakerPaymentNotification.create()

        self.mercado_pago_service.process_external_feedback.side_effect = Exception(
            "Processing error"
        )

        with pytest.raises(Exception, match="Processing error"):
            await proccess_mercado_pago_message_service.process(notification)

        self.save_webhook_notification_service.process.assert_called_once_with(
            notification.to_dict()
        )
        self.mercado_pago_service.process_external_feedback.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_skip_processing_when_notification_type_is_missing(
        self, proccess_mercado_pago_message_service: ProccessMercadoPagoMessageService
    ):
        notification = FakerPaymentNotification.create({"type": ""})

        await proccess_mercado_pago_message_service.process(notification)

        self.save_webhook_notification_service.process.assert_called_once_with(
            notification.to_dict()
        )
        self.mercado_pago_service.process_external_feedback.assert_not_called()
        self.process_external_payment_result_service.process.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_skip_processing_when_notification_type_is_not_payment(
        self, proccess_mercado_pago_message_service: ProccessMercadoPagoMessageService
    ):
        notification = FakerPaymentNotification.create({"type": "order"})

        await proccess_mercado_pago_message_service.process(notification)

        self.save_webhook_notification_service.process.assert_called_once_with(
            notification.to_dict()
        )
        self.mercado_pago_service.process_external_feedback.assert_not_called()
        self.process_external_payment_result_service.process.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_continue_processing_when_save_notification_fails(
        self, proccess_mercado_pago_message_service: ProccessMercadoPagoMessageService
    ):
        notification = FakerPaymentNotification.create()

        self.save_webhook_notification_service.process.side_effect = Exception(
            "Save error"
        )

        result_status = FakerExternalOrderPaymentResult.create(
            status=PaymentStatus.PAID
        )
        self.mercado_pago_service.process_external_feedback.return_value = result_status

        await proccess_mercado_pago_message_service.process(notification)

        self.save_webhook_notification_service.process.assert_called_once_with(
            notification.to_dict()
        )
        self.mercado_pago_service.process_external_feedback.assert_called_once()
        self.process_external_payment_result_service.process.assert_called_once_with(
            result_status
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_process_notification_with_payment_type_in_string(
        self, proccess_mercado_pago_message_service: ProccessMercadoPagoMessageService
    ):
        notification = FakerPaymentNotification.create({"type": "payment.created"})

        result_status = FakerExternalOrderPaymentResult.create(
            status=PaymentStatus.PENDING
        )
        self.mercado_pago_service.process_external_feedback.return_value = result_status

        await proccess_mercado_pago_message_service.process(notification)

        self.mercado_pago_service.process_external_feedback.assert_called_once()
        self.process_external_payment_result_service.process.assert_called_once_with(
            result_status
        )
