from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

from modules.client.entities.client_entity import ClientEntity

class ClientDto(BaseModel):
    id: str = Field(default=None, description="ID do cliente.")
    name: str = Field(..., description="Nome identificador do sistema solicitante.")
    notification_url: str = Field(
        ..., description="URL para qual atualizações de pagamentos serão enviadas. (Webhook)"
    )
    created_at: Optional[datetime] = Field(default=None, description="Data de criação do cliente.")

    @staticmethod
    def from_client_entity(entity: ClientEntity) -> "ClientDto":
        return ClientDto(
            id=entity.id,
            name=entity.name,
            notification_url=entity.notification_url,
            created_at=entity.created_at,
        )