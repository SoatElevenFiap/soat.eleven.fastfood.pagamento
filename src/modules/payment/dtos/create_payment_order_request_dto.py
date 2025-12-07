from typing import List, Optional

from pydantic import BaseModel, Field

from modules.external_provider.enums import ExternalProvider
from modules.payment.models.payment_item_model import PaymentItemModel


class CreatePaymentOrderRequestDto(BaseModel):
    end_to_end_id: str = Field(
        ..., description="Id externo para identificação posterior"
    )
    client_id: str = Field(..., description="ID do cliente")
    items: List[PaymentItemModel] = Field(
        ..., description="Itens relacionados ao pagamento"
    )
    description: Optional[str] = Field(
        default=None,
        description="Descrição do pagamento para facilitar identificação posterior",
    )
    provider: Optional[ExternalProvider] = Field(
        default=ExternalProvider.MERCADOPAGO,
        description="Provedor de pagamento, se não fornecido, será usado o Mercado Pago",
    )
    metadata: Optional[dict] = Field(default={}, description="Metadados do pedido")
