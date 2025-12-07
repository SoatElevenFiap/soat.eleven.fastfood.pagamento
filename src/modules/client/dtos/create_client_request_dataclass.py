from pydantic import BaseModel, Field


class CreateClientRequestDto(BaseModel):
    name: str = Field(..., description="Nome identificador do sistema solicitante.", min_length=3, max_length=100)
    notification_url: str = Field(..., description="URL para qual atualizações de pedidos serão enviadas.", pattern=r"^https?://.*$")