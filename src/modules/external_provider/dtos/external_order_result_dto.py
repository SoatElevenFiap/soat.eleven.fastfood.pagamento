from typing import Optional

from pydantic import BaseModel, Field

from modules.external_provider.enums import ExternalProvider


class ExternalOrderResultDto(BaseModel):
    id: str
    status: str
    amount: float
    provider: ExternalProvider
    provider_result: Optional[dict] = Field(
        default={}, description="Resultado do pedido do provedor externo"
    )
