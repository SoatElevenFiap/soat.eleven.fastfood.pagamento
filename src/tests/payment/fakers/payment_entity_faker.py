from typing import Optional
from faker import Faker

from modules.payment.entities.payment_entity import PaymentEntity
from modules.payment.enums import PaymentStatus
from modules.external_provider.enums import ExternalProvider


class FakerPaymentEntity:
    @staticmethod
    def create(
        id: Optional[str] = None,
        client_id: Optional[str] = None,
        end_to_end_id: Optional[str] = None,
        external_reference_id: Optional[str] = None,
        value: Optional[float] = None,
        provider: Optional[ExternalProvider] = None,
        status: Optional[PaymentStatus] = None,
        redirect_url: Optional[str] = None,
    ) -> PaymentEntity:
        faker = Faker()
        
        payment = PaymentEntity(
            client_id=client_id or faker.uuid4(),
            end_to_end_id=end_to_end_id or faker.uuid4(),
            external_reference_id=external_reference_id or faker.uuid4(),
            value=value or round(faker.random.uniform(10.0, 1000.0), 2),
            provider=provider or ExternalProvider.MERCADOPAGO,
            status=status or PaymentStatus.PENDING,
            redirect_url=redirect_url or faker.url(),
        )
        if id:
            payment.id = id
        return payment

