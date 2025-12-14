import pytest
from pytest_mock import MockFixture

from modules.payment.providers.get_payment_by_end_to_end_id_service import (
    GetPaymentByEndToEndIdServiceProvider,
)
from modules.payment.providers.get_payment_service_provider import (
    GetPaymentServiceProvider,
)
from modules.payment.services.application.get_payment_service import (
    GetPaymentApplicationService,
)
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException
from tests.payment.fakers import FakerPaymentEntity


@pytest.mark.asyncio
class TestGetPaymentApplicationService:
    @pytest.fixture
    def get_payment_application_service(
        self, mocker: MockFixture
    ) -> GetPaymentApplicationService:
        self.get_payment_service = mocker.MagicMock(spec=GetPaymentServiceProvider)
        self.get_payment_service.process = mocker.AsyncMock()

        self.get_payment_by_end_to_end_id_service = mocker.MagicMock(
            spec=GetPaymentByEndToEndIdServiceProvider
        )
        self.get_payment_by_end_to_end_id_service.process = mocker.AsyncMock()

        return GetPaymentApplicationService(
            get_payment_service=self.get_payment_service,
            get_payment_by_end_to_end_id_service=self.get_payment_by_end_to_end_id_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_by_id_successfully(
        self, get_payment_application_service: GetPaymentApplicationService
    ):
        from faker import Faker
        faker = Faker()
        payment_id = faker.uuid4()
        fake_payment = FakerPaymentEntity.create(id=payment_id)
        self.get_payment_service.process.return_value = fake_payment

        result = await get_payment_application_service.process(id=payment_id)

        self.get_payment_service.process.assert_called_once_with(payment_id)
        self.get_payment_by_end_to_end_id_service.process.assert_not_called()
        assert result.id == fake_payment.id

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_by_end_to_end_id_successfully(
        self, get_payment_application_service: GetPaymentApplicationService
    ):
        from faker import Faker
        faker = Faker()
        payment_id = faker.uuid4()
        fake_payment = FakerPaymentEntity.create(id=payment_id)
        self.get_payment_by_end_to_end_id_service.process.return_value = fake_payment

        result = await get_payment_application_service.process(
            end_to_end_id=fake_payment.end_to_end_id
        )

        self.get_payment_by_end_to_end_id_service.process.assert_called_once_with(
            fake_payment.end_to_end_id
        )
        self.get_payment_service.process.assert_not_called()
        assert result.id == fake_payment.id

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_raise_exception_when_no_parameters_provided(
        self, get_payment_application_service: GetPaymentApplicationService
    ):
        with pytest.raises(DomainException) as exc_info:
            await get_payment_application_service.process()

        assert exc_info.value.code == ExceptionConstants.INVALID_REQUEST
        assert "Either 'id' or 'end_to_end_id'" in exc_info.value.message
        self.get_payment_service.process.assert_not_called()
        self.get_payment_by_end_to_end_id_service.process.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_raise_exception_when_both_parameters_provided(
        self, get_payment_application_service: GetPaymentApplicationService
    ):
        with pytest.raises(DomainException) as exc_info:
            await get_payment_application_service.process(
                id="payment-id", end_to_end_id="e2e-id"
            )

        assert exc_info.value.code == ExceptionConstants.INVALID_REQUEST
        assert "Only one parameter" in exc_info.value.message
        self.get_payment_service.process.assert_not_called()
        self.get_payment_by_end_to_end_id_service.process.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_raise_exception_when_payment_not_found_by_id(
        self, get_payment_application_service: GetPaymentApplicationService
    ):
        payment_id = "non-existent-id"
        self.get_payment_service.process.return_value = None

        with pytest.raises(DomainException) as exc_info:
            await get_payment_application_service.process(id=payment_id)

        assert exc_info.value.code == ExceptionConstants.PAYMENT_NOT_FOUND
        assert payment_id in exc_info.value.message
        self.get_payment_service.process.assert_called_once_with(payment_id)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_raise_exception_when_payment_not_found_by_end_to_end_id(
        self, get_payment_application_service: GetPaymentApplicationService
    ):
        end_to_end_id = "non-existent-e2e-id"
        self.get_payment_by_end_to_end_id_service.process.return_value = None

        with pytest.raises(DomainException) as exc_info:
            await get_payment_application_service.process(end_to_end_id=end_to_end_id)

        assert exc_info.value.code == ExceptionConstants.PAYMENT_NOT_FOUND
        assert end_to_end_id in exc_info.value.message
        self.get_payment_by_end_to_end_id_service.process.assert_called_once_with(
            end_to_end_id
        )

