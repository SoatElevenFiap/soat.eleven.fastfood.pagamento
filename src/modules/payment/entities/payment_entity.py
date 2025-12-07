from typing import Optional

from pydantic import Field

from modules.external_provider.enums import ExternalProvider
from modules.payment.enums import PaymentStatus
from modules.shared.adapters import EntityAdapter


class PaymentEntity(EntityAdapter):
    client_id: str
    end_to_end_id: str
    external_reference_id: str
    value: float
    provider: ExternalProvider
    status: PaymentStatus
    redirect_url: Optional[str] = Field(default=None)
