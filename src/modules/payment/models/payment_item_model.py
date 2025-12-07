from typing import Optional

from pydantic import BaseModel, Field


class PaymentItemModel(BaseModel):
    id: Optional[str] = Field(default=None, description="ID do item")
    title: str = Field(
        ..., description="Título identificador do item", min_length=1, max_length=100
    )
    quantity: int = Field(..., description="Quantidade do item", ge=1)
    unit_price: float = Field(
        ..., description="Preço unitário do item", ge=0.01, le=1000000
    )
