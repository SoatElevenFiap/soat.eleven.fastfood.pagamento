import pytest
from faker import Faker
from pytest_mock import MockFixture
from modules.external_provider.services.domain.get_external_provider_service import (
    GetExternalProviderService,
)
from modules.external_provider.adapters.external_provider_adapter import (
    ExternalProviderAdapter,
)
from modules.external_provider.enums import ExternalProvider
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException


@pytest.mark.asyncio
class TestGetExternalProviderService:
    @pytest.fixture
    def get_external_provider_service(self, mocker: MockFixture) -> GetExternalProviderService:
        self.faker = Faker()

        self.mercado_pago_service = mocker.MagicMock(spec=ExternalProviderAdapter)

        return GetExternalProviderService(mercado_pago_service=self.mercado_pago_service)

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.external_provider
    async def test_get_mercado_pago_provider_successfully(
        self, get_external_provider_service: GetExternalProviderService
    ):
        sut = await get_external_provider_service.process(ExternalProvider.MERCADOPAGO)

        assert sut == self.mercado_pago_service, "Should return MercadoPago service"

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.external_provider
    async def test_raise_exception_when_provider_not_supported(
        self, get_external_provider_service: GetExternalProviderService
    ):
        invalid_provider = "invalid_provider"

        with pytest.raises(DomainException) as exc_info:
            await get_external_provider_service.process(invalid_provider)

        assert exc_info.value.code == ExceptionConstants.INVALID_EXTERNAL_PROVIDER
        assert invalid_provider in exc_info.value.message

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.external_provider
    async def test_raise_exception_when_provider_is_empty_string(
        self, get_external_provider_service: GetExternalProviderService
    ):
        with pytest.raises(DomainException) as exc_info:
            await get_external_provider_service.process("")

        assert exc_info.value.code == ExceptionConstants.INVALID_EXTERNAL_PROVIDER

    @pytest.mark.asyncio
    @pytest.mark.domain
    @pytest.mark.external_provider
    async def test_raise_exception_when_provider_not_implemented(
        self, get_external_provider_service: GetExternalProviderService
    ):
        with pytest.raises(DomainException) as exc_info:
            await get_external_provider_service.process(ExternalProvider.PAGSEGURO)

        assert exc_info.value.code == ExceptionConstants.INVALID_EXTERNAL_PROVIDER
        assert "PAGSEGURO" in exc_info.value.message or "pagseguro" in exc_info.value.message
