from typing import Optional

from pydantic import BaseModel, Field

from modules.external_provider.enums import ExternalProvider
from modules.external_provider.enums.external_provider_payment_status import (
    ExternalProviderPaymentStatus,
)


class ExternalOrderResultDto(BaseModel):
    id: str
    status: ExternalProviderPaymentStatus
    amount: float
    provider: ExternalProvider
    provider_result: Optional[dict] = Field(
        default={}, description="Resultado do pedido do provedor externo"
    )
