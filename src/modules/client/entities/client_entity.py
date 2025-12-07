from pydantic import Field

from modules.shared.adapters import EntityAdapter


class ClientEntity(EntityAdapter):
    name: str = Field(..., description="Nome identificador do sistema solicitante.")
    notification_url: str = Field(
        ..., description="URL para qual atualizações de pagamentos serão enviadas."
    )
