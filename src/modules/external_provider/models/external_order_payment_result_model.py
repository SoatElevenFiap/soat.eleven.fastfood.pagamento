from pydantic import BaseModel

from modules.external_provider.enums import ExternalProvider
from modules.payment.enums import PaymentStatus


class ExternalOrderPaymentResultModel(BaseModel):
    end_to_end_id: str
    status: PaymentStatus
    provider: ExternalProvider
