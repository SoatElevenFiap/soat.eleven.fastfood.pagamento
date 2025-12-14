from typing import Optional
from faker import Faker

from modules.external_provider.entities.external_order import ExternalOrderEntity
from modules.external_provider.enums import ExternalProvider
from modules.payment.enums import PaymentStatus


class FakerExternalOrderEntity:
    @staticmethod
    def create(
        id: Optional[str] = None,
        client_id: Optional[str] = None,
        end_to_end_id: Optional[str] = None,
        status: Optional[PaymentStatus] = None,
        amount: Optional[float] = None,
        redirect_url: Optional[str] = None,
        provider: Optional[ExternalProvider] = None,
        provider_result: Optional[dict] = None,
    ) -> ExternalOrderEntity:
        faker = Faker()

        return ExternalOrderEntity(
            id=id or faker.uuid4(),
            client_id=client_id or faker.uuid4(),
            end_to_end_id=end_to_end_id or faker.uuid4(),
            status=status or PaymentStatus.PENDING,
            amount=amount or round(faker.random.uniform(10.0, 1000.0), 2),
            redirect_url=redirect_url or faker.url(),
            provider=provider or ExternalProvider.MERCADOPAGO,
            provider_result=provider_result or {},
        )

