import pytest
from pytest_mock import MockFixture

from modules.webhook.controllers.mercado_pago_controller import (
    MercadoPagoWebhookController,
)
from modules.webhook.providers.process_mercado_pago_message_service_provider import (
    ProccessMercadoPagoMessageServiceProvider,
)
from tests.webhook.fakers import FakerPaymentNotification


@pytest.mark.asyncio
class TestMercadoPagoWebhookController:
    @pytest.fixture
    def mercado_pago_webhook_controller(self) -> MercadoPagoWebhookController:
        return MercadoPagoWebhookController()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_mercado_pago_webhook_successfully(
        self,
        mercado_pago_webhook_controller: MercadoPagoWebhookController,
        mocker: MockFixture,
    ):
        notification = FakerPaymentNotification.create()

        mock_service = mocker.MagicMock(spec=ProccessMercadoPagoMessageServiceProvider)
        mock_service.process = mocker.AsyncMock()

        result = await mercado_pago_webhook_controller.mercado_pago_webhook(
            notification, mock_service
        )

        mock_service.process.assert_called_once_with(notification)
        assert result == {"message": "External feedback processed successfully"}

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_mercado_pago_webhook_with_payment_notification(
        self,
        mercado_pago_webhook_controller: MercadoPagoWebhookController,
        mocker: MockFixture,
    ):
        notification = FakerPaymentNotification.create(
            payload={"type": "payment", "action": "payment.created"}
        )

        mock_service = mocker.MagicMock(spec=ProccessMercadoPagoMessageServiceProvider)
        mock_service.process = mocker.AsyncMock()

        result = await mercado_pago_webhook_controller.mercado_pago_webhook(
            notification, mock_service
        )

        mock_service.process.assert_called_once_with(notification)
        assert result == {"message": "External feedback processed successfully"}

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_mercado_pago_webhook_with_order_notification(
        self,
        mercado_pago_webhook_controller: MercadoPagoWebhookController,
        mocker: MockFixture,
    ):
        notification = FakerPaymentNotification.create(
            payload={"type": "order", "action": "order.created"}
        )

        mock_service = mocker.MagicMock(spec=ProccessMercadoPagoMessageServiceProvider)
        mock_service.process = mocker.AsyncMock()

        result = await mercado_pago_webhook_controller.mercado_pago_webhook(
            notification, mock_service
        )

        mock_service.process.assert_called_once_with(notification)
        assert result == {"message": "External feedback processed successfully"}
