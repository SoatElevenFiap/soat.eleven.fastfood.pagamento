from pydantic import BaseModel

from modules.external_provider.enums import ExternalProvider
from modules.external_provider.enums.external_provider_payment_status import (
    ExternalProviderPaymentStatus,
)


class ExternalOrderPaymentResultModel(BaseModel):
    end_to_end_id: str
    status: ExternalProviderPaymentStatus
    provider: ExternalProvider
