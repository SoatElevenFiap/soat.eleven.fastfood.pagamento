from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from modules.external_provider.enums import ExternalProvider
from modules.payment.entities import PaymentEntity
from modules.payment.enums.payment_status_enum import PaymentStatus


class GetPaymentByEndToEndIdResponseDto(BaseModel):
    id: str = Field(..., description="ID do pagamento")
    end_to_end_id: str = Field(
        ..., description="Id externo para identificação posterior"
    )
    external_reference_id: str = Field(
        ..., description="ID de referência do provedor externo"
    )
    client_id: str = Field(..., description="ID do cliente")
    value: float = Field(..., description="Valor do pagamento")
    provider: ExternalProvider = Field(..., description="Provedor de pagamento")
    status: PaymentStatus = Field(..., description="Status do pagamento")
    redirect_url: Optional[str] = Field(
        default=None, description="URL de redirecionamento do pagamento"
    )
    created_at: Optional[datetime] = Field(
        default=None, description="Data de criação do pagamento"
    )
    updated_at: Optional[datetime] = Field(
        default=None, description="Data de atualização do pagamento"
    )

    @staticmethod
    def from_payment_entity(entity: PaymentEntity) -> "GetPaymentByEndToEndIdResponseDto":
        return GetPaymentByEndToEndIdResponseDto(
            id=entity.id,
            end_to_end_id=entity.end_to_end_id,
            external_reference_id=entity.external_reference_id,
            client_id=entity.client_id,
            value=entity.value,
            provider=entity.provider,
            status=entity.status,
            redirect_url=entity.redirect_url,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
