from typing import Optional

from pydantic import BaseModel, Field

from modules.external_provider.enums import ExternalProvider
from modules.payment.enums import PaymentStatus


class ExternalOrderEntity(BaseModel):
    id: str
    client_id: str
    end_to_end_id: str
    status: PaymentStatus
    amount: float
    redirect_url: Optional[str] = Field(default=None)
    provider: ExternalProvider
    provider_result: Optional[dict] = Field(default={})
