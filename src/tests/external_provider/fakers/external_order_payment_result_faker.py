from typing import Optional

from faker import Faker

from modules.external_provider.enums import ExternalProvider
from modules.external_provider.models import ExternalOrderPaymentResultModel
from modules.payment.enums import PaymentStatus


class FakerExternalOrderPaymentResult:
    @staticmethod
    def create(
        end_to_end_id: Optional[str] = None,
        status: Optional[PaymentStatus] = None,
        provider: Optional[ExternalProvider] = None,
    ) -> ExternalOrderPaymentResultModel:
        faker = Faker()

        return ExternalOrderPaymentResultModel(
            end_to_end_id=end_to_end_id or faker.uuid4(),
            status=status or PaymentStatus.PAID,
            provider=provider or ExternalProvider.MERCADOPAGO,
        )
