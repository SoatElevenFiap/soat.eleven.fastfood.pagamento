from typing import List

from pydantic import BaseModel, Field

from modules.payment.models.payment_item_model import PaymentItemModel


class CreateExternalOrderModel(BaseModel):
    end_to_end_id: str = Field(
        ..., description="Id externo para identificação posterior"
    )
    client_id: str = Field(..., description="ID do cliente")
    items: List[PaymentItemModel] = Field(
        ..., description="Itens relacionados ao pagamento"
    )
