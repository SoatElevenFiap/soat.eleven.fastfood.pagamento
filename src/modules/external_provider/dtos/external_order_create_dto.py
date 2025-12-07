from pydantic import BaseModel, Field


class ExternalOrderCreateDto(BaseModel):
    value: float = Field(..., description="Valor do pedido", ge=0.01, le=1000000)
