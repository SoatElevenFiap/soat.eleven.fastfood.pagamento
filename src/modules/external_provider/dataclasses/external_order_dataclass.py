from pydantic import BaseModel

from modules.external_provider.enums.external_provider_payment_status import (
    ExternalProviderPaymentStatus,
)


class ExternalOrderDataclass(BaseModel):
    id: str
    status: ExternalProviderPaymentStatus
    amount: float
