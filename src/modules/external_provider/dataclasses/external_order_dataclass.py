from modules.external_provider.enums.external_provider_payment_status import ExternalProviderPaymentStatus
from pydantic import BaseModel

class ExternalOrderDataclass(BaseModel):
    id: str
    status: ExternalProviderPaymentStatus
    amount: float