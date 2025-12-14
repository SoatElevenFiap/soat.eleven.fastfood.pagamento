import pytest
from pytest_mock import MockFixture

from modules.payment.constants import PaymentCacheKeys
from modules.payment.entities.payment_entity import PaymentEntity
from modules.payment.enums import PaymentStatus
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.providers.mongo_service_provider import MongoServiceProvider
from modules.shared.services.cache_manager import CacheManagerService
from tests.payment.fakers import FakerPaymentEntity


@pytest.mark.asyncio
class TestPaymentRepository:
    @pytest.fixture
    def payment_repository(self, mocker: MockFixture) -> PaymentRepository:
        self.mongo_service = mocker.MagicMock(spec=MongoServiceProvider)
        self.mongo_service.add_document = mocker.AsyncMock()
        self.mongo_service.get_document = mocker.AsyncMock()
        self.mongo_service.update_document = mocker.AsyncMock()

        self.cache_manager_service = mocker.MagicMock(spec=CacheManagerService)
        self.cache_manager_service.build_cache_operation = mocker.AsyncMock()
        self.cache_manager_service.set_value = mocker.Mock()

        return PaymentRepository(
            mongo_service=self.mongo_service,
            cache_manager_service=self.cache_manager_service,
        )

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_add_payment_successfully(
        self, payment_repository: PaymentRepository
    ):
        payment_id = "test-payment-id"
        fake_payment = FakerPaymentEntity.create(id=payment_id)

        self.mongo_service.add_document.return_value = payment_id
        self.cache_manager_service.build_cache_operation.return_value = fake_payment

        result = await payment_repository.add_payment(fake_payment)

        self.mongo_service.add_document.assert_called_once()
        call_args = self.mongo_service.add_document.call_args
        assert call_args[0][0] == "payments"
        assert "id" not in call_args[0][1]
        assert self.cache_manager_service.set_value.call_count == 2
        assert result == fake_payment

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_successfully(
        self, payment_repository: PaymentRepository
    ):
        payment_id = "test-payment-id"
        fake_payment = FakerPaymentEntity.create(id=payment_id)

        self.cache_manager_service.build_cache_operation.return_value = fake_payment

        result = await payment_repository.get_payment(payment_id)

        self.cache_manager_service.build_cache_operation.assert_called_once()
        call_args = self.cache_manager_service.build_cache_operation.call_args
        assert call_args.kwargs["key"] == PaymentCacheKeys.payment_key_for(payment_id)
        assert call_args.kwargs["entity_class"] == PaymentEntity
        assert result == fake_payment

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_returns_none_when_not_found(
        self, payment_repository: PaymentRepository
    ):
        payment_id = "non-existent-id"

        self.cache_manager_service.build_cache_operation.return_value = None

        result = await payment_repository.get_payment(payment_id)

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_by_end_to_end_id_successfully(
        self, payment_repository: PaymentRepository
    ):
        fake_payment = FakerPaymentEntity.create()
        end_to_end_id = fake_payment.end_to_end_id

        self.cache_manager_service.build_cache_operation.return_value = fake_payment

        result = await payment_repository.get_payment_by_end_to_end_id(end_to_end_id)

        self.cache_manager_service.build_cache_operation.assert_called_once()
        call_args = self.cache_manager_service.build_cache_operation.call_args
        assert call_args.kwargs[
            "key"
        ] == PaymentCacheKeys.payment_by_end_to_end_id_key_for(end_to_end_id)
        assert call_args.kwargs["entity_class"] == PaymentEntity
        assert result == fake_payment

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_payment_by_end_to_end_id_returns_none_when_not_found(
        self, payment_repository: PaymentRepository
    ):
        end_to_end_id = "non-existent-e2e-id"

        self.cache_manager_service.build_cache_operation.return_value = None

        result = await payment_repository.get_payment_by_end_to_end_id(end_to_end_id)

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_make_payment_paid_successfully(
        self, payment_repository: PaymentRepository
    ):
        payment_id = "test-payment-id"
        updated_payment = FakerPaymentEntity.create(
            id=payment_id, status=PaymentStatus.PAID
        )
        updated_payment_dict = updated_payment.model_dump(by_alias=True)
        updated_payment_dict["_id"] = payment_id

        self.mongo_service.update_document.return_value = updated_payment_dict

        result = await payment_repository.make_payment_paid(payment_id)

        self.mongo_service.update_document.assert_called_once()
        call_args = self.mongo_service.update_document.call_args
        assert call_args[0][0] == "payments"
        assert call_args[0][1] == {"id": payment_id}
        assert call_args[0][2]["status"] == PaymentStatus.PAID
        assert self.cache_manager_service.set_value.call_count == 2
        assert result.status == PaymentStatus.PAID
        assert result.id == payment_id

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_make_payment_paid_returns_none_when_not_found(
        self, payment_repository: PaymentRepository
    ):
        payment_id = "non-existent-id"

        self.mongo_service.update_document.return_value = None

        result = await payment_repository.make_payment_paid(payment_id)

        assert result is None
        self.cache_manager_service.set_value.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_change_payment_status_successfully(
        self, payment_repository: PaymentRepository
    ):
        payment_id = "test-payment-id"
        new_status = PaymentStatus.FAILED
        updated_payment = FakerPaymentEntity.create(id=payment_id, status=new_status)
        updated_payment_dict = updated_payment.model_dump(by_alias=True)
        updated_payment_dict["_id"] = payment_id

        self.mongo_service.update_document.return_value = updated_payment_dict

        result = await payment_repository.change_payment_status(payment_id, new_status)

        self.mongo_service.update_document.assert_called_once()
        call_args = self.mongo_service.update_document.call_args
        assert call_args[0][0] == "payments"
        assert call_args[0][1] == {"id": payment_id}
        assert call_args[0][2]["status"] == new_status
        assert self.cache_manager_service.set_value.call_count == 2
        assert result.status == new_status
        assert result.id == payment_id

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_change_payment_status_returns_none_when_not_found(
        self, payment_repository: PaymentRepository
    ):
        payment_id = "non-existent-id"
        new_status = PaymentStatus.PAID

        self.mongo_service.update_document.return_value = None

        result = await payment_repository.change_payment_status(payment_id, new_status)

        assert result is None
        self.cache_manager_service.set_value.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_change_payment_status_to_cancelled(
        self, payment_repository: PaymentRepository
    ):
        payment_id = "test-payment-id"
        new_status = PaymentStatus.CANCELLED
        updated_payment = FakerPaymentEntity.create(id=payment_id, status=new_status)
        updated_payment_dict = updated_payment.model_dump(by_alias=True)
        updated_payment_dict["_id"] = payment_id

        self.mongo_service.update_document.return_value = updated_payment_dict

        result = await payment_repository.change_payment_status(payment_id, new_status)

        assert result.status == new_status
        assert result.id == payment_id
        assert self.cache_manager_service.set_value.call_count == 2
