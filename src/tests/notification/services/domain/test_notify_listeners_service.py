import pytest
import httpx
from pytest_mock import MockFixture

from modules.notification.services.domain.notify_listeners_service import (
    NotifyListenersService,
)
from modules.client.services.domain.get_client_service import GetClientService
from modules.payment.enums import PaymentStatus
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException
from tests.client.fakers import FakerClient
from tests.payment.fakers import FakerPaymentEntity


@pytest.mark.asyncio
class TestNotifyListenersService:
    @pytest.fixture
    def notify_listeners_service(
        self, mocker: MockFixture
    ) -> NotifyListenersService:
        self.get_client_service = mocker.MagicMock(spec=GetClientService)
        self.get_client_service.process = mocker.AsyncMock()

        return NotifyListenersService(get_client_service=self.get_client_service)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_notify_client_successfully(
        self, notify_listeners_service: NotifyListenersService, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create()
        fake_client = FakerClient.create()

        self.get_client_service.process.return_value = fake_client

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = mocker.Mock()

        mock_http_client = mocker.MagicMock()
        mock_http_client.post = mocker.AsyncMock(return_value=mock_response)
        mock_http_client.__aenter__ = mocker.AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = mocker.AsyncMock(return_value=None)

        mocker.patch("httpx.AsyncClient", return_value=mock_http_client)

        await notify_listeners_service.process(fake_payment)

        self.get_client_service.process.assert_called_once_with(fake_payment.client_id)
        mock_http_client.post.assert_called_once()
        call_args = mock_http_client.post.call_args
        assert call_args[0][0] == fake_client.notification_url
        assert call_args[1]["json"] == fake_payment.model_dump(mode="json")
        mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_raise_exception_when_client_not_found(
        self, notify_listeners_service: NotifyListenersService
    ):
        fake_payment = FakerPaymentEntity.create()
        self.get_client_service.process.return_value = None

        with pytest.raises(DomainException) as exc_info:
            await notify_listeners_service.process(fake_payment)

        assert exc_info.value.code == ExceptionConstants.INVALID_CLIENT
        assert fake_payment.client_id in exc_info.value.message
        self.get_client_service.process.assert_called_once_with(fake_payment.client_id)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_handle_http_error_gracefully(
        self, notify_listeners_service: NotifyListenersService, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create()
        fake_client = FakerClient.create()

        self.get_client_service.process.return_value = fake_client

        mock_http_client = mocker.MagicMock()
        mock_http_client.post = mocker.AsyncMock(
            side_effect=httpx.HTTPError("Connection error")
        )
        mock_http_client.__aenter__ = mocker.AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = mocker.AsyncMock(return_value=None)

        mocker.patch("httpx.AsyncClient", return_value=mock_http_client)

        await notify_listeners_service.process(fake_payment)

        self.get_client_service.process.assert_called_once_with(fake_payment.client_id)
        mock_http_client.post.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_handle_http_status_error_gracefully(
        self, notify_listeners_service: NotifyListenersService, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create()
        fake_client = FakerClient.create()

        self.get_client_service.process.return_value = fake_client

        mock_response = mocker.MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status = mocker.Mock(
            side_effect=httpx.HTTPStatusError(
                "Server error", request=mocker.MagicMock(), response=mock_response
            )
        )

        mock_http_client = mocker.MagicMock()
        mock_http_client.post = mocker.AsyncMock(return_value=mock_response)
        mock_http_client.__aenter__ = mocker.AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = mocker.AsyncMock(return_value=None)

        mocker.patch("httpx.AsyncClient", return_value=mock_http_client)

        await notify_listeners_service.process(fake_payment)

        self.get_client_service.process.assert_called_once_with(fake_payment.client_id)
        mock_http_client.post.assert_called_once()
        mock_response.raise_for_status.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_handle_timeout_error_gracefully(
        self, notify_listeners_service: NotifyListenersService, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create()
        fake_client = FakerClient.create()

        self.get_client_service.process.return_value = fake_client

        mock_http_client = mocker.MagicMock()
        mock_http_client.post = mocker.AsyncMock(
            side_effect=httpx.TimeoutException("Request timeout")
        )
        mock_http_client.__aenter__ = mocker.AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = mocker.AsyncMock(return_value=None)

        mocker.patch("httpx.AsyncClient", return_value=mock_http_client)

        await notify_listeners_service.process(fake_payment)

        self.get_client_service.process.assert_called_once_with(fake_payment.client_id)
        mock_http_client.post.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_handle_generic_exception_gracefully(
        self, notify_listeners_service: NotifyListenersService, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create()
        fake_client = FakerClient.create()

        self.get_client_service.process.return_value = fake_client

        mock_http_client = mocker.MagicMock()
        mock_http_client.post = mocker.AsyncMock(
            side_effect=Exception("Unexpected error")
        )
        mock_http_client.__aenter__ = mocker.AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = mocker.AsyncMock(return_value=None)

        mocker.patch("httpx.AsyncClient", return_value=mock_http_client)

        await notify_listeners_service.process(fake_payment)

        self.get_client_service.process.assert_called_once_with(fake_payment.client_id)
        mock_http_client.post.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_send_correct_payment_data_to_client(
        self, notify_listeners_service: NotifyListenersService, mocker: MockFixture
    ):
        fake_payment = FakerPaymentEntity.create(
            status=PaymentStatus.PAID, value=150.50
        )
        fake_client = FakerClient.create()

        self.get_client_service.process.return_value = fake_client

        mock_response = mocker.MagicMock()
        mock_response.status_code = 200
        mock_response.raise_for_status = mocker.Mock()

        mock_http_client = mocker.MagicMock()
        mock_http_client.post = mocker.AsyncMock(return_value=mock_response)
        mock_http_client.__aenter__ = mocker.AsyncMock(return_value=mock_http_client)
        mock_http_client.__aexit__ = mocker.AsyncMock(return_value=None)

        mocker.patch("httpx.AsyncClient", return_value=mock_http_client)

        await notify_listeners_service.process(fake_payment)

        call_args = mock_http_client.post.call_args
        assert call_args[0][0] == fake_client.notification_url
        payment_data = call_args[1]["json"]
        assert payment_data["client_id"] == fake_payment.client_id
        assert payment_data["end_to_end_id"] == fake_payment.end_to_end_id
        assert payment_data["value"] == fake_payment.value
        assert payment_data["status"] == fake_payment.status.value

