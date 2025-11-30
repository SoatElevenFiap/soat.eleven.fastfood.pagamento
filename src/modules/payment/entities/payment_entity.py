from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from modules.external_provider.enums import ExternalProvider
from modules.payment.enums import PaymentStatus


class PaymentEntity(BaseModel):
    id: str
    end_to_end_id: Optional[str] = None
    amount: float
    provider: ExternalProvider
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime
