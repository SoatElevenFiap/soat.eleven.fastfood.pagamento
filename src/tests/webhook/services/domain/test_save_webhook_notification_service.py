from datetime import UTC, datetime

import pytest
from pytest_mock import MockFixture

from modules.external_provider.enums import ExternalProvider
from modules.shared.services.mongo.mongo_service import MongoService
from modules.webhook.services.domain.save_webhook_notification import (
    SaveWebhookNotificationService,
)
from tests.webhook.fakers import FakerPaymentNotification


@pytest.mark.asyncio
class TestSaveWebhookNotificationService:
    @pytest.fixture
    def save_webhook_notification_service(
        self, mocker: MockFixture
    ) -> SaveWebhookNotificationService:
        self.mongo_service = mocker.MagicMock(spec=MongoService)
        self.mongo_service.add_document = mocker.AsyncMock(return_value="document_id")

        return SaveWebhookNotificationService(mongo_service=self.mongo_service)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_save_notification_with_dict_successfully(
        self, save_webhook_notification_service: SaveWebhookNotificationService
    ):
        notification = FakerPaymentNotification.create()

        await save_webhook_notification_service.process(notification)

        self.mongo_service.add_document.assert_called_once()
        call_args = self.mongo_service.add_document.call_args

        assert call_args[0][0] == "notifications"
        document = call_args[0][1]

        assert document["notification"] == notification
        assert document["provider"] == ExternalProvider.MERCADOPAGO
        assert isinstance(document["created_at"], datetime)
        assert document["created_at"].tzinfo == UTC

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_save_notification_with_string_successfully(
        self, save_webhook_notification_service: SaveWebhookNotificationService
    ):
        notification = '{"id": 123456, "type": "payment"}'

        await save_webhook_notification_service.process(notification)

        self.mongo_service.add_document.assert_called_once()
        call_args = self.mongo_service.add_document.call_args

        assert call_args[0][0] == "notifications"
        document = call_args[0][1]

        assert document["notification"] == notification
        assert document["provider"] == ExternalProvider.MERCADOPAGO
        assert isinstance(document["created_at"], datetime)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_save_notification_with_list_successfully(
        self, save_webhook_notification_service: SaveWebhookNotificationService
    ):
        notification = [
            {"id": 123456, "type": "payment"},
            {"id": 789012, "type": "order"},
        ]

        await save_webhook_notification_service.process(notification)

        self.mongo_service.add_document.assert_called_once()
        call_args = self.mongo_service.add_document.call_args

        assert call_args[0][0] == "notifications"
        document = call_args[0][1]

        assert document["notification"] == notification
        assert document["provider"] == ExternalProvider.MERCADOPAGO
        assert isinstance(document["created_at"], datetime)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_save_notification_with_empty_dict(
        self, save_webhook_notification_service: SaveWebhookNotificationService
    ):
        notification = {}

        await save_webhook_notification_service.process(notification)

        self.mongo_service.add_document.assert_called_once()
        call_args = self.mongo_service.add_document.call_args

        assert call_args[0][0] == "notifications"
        document = call_args[0][1]

        assert document["notification"] == notification
        assert document["provider"] == ExternalProvider.MERCADOPAGO

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_save_notification_uses_mercado_pago_provider(
        self, save_webhook_notification_service: SaveWebhookNotificationService
    ):
        notification = FakerPaymentNotification.create()

        await save_webhook_notification_service.process(notification)

        call_args = self.mongo_service.add_document.call_args
        document = call_args[0][1]

        assert document["provider"] == ExternalProvider.MERCADOPAGO
