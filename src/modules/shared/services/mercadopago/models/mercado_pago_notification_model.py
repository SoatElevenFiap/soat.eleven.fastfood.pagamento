from typing import Optional

from pydantic import BaseModel


class MercadoPagoNotificationModel(BaseModel):
    id: int
    action: str
    api_version: str
    data: dict
    date_created: str
    live_mode: bool
    type: str
    user_id: int

    def has_type(self) -> bool:
        """Verifica se a notificação possui um tipo definido."""
        return bool(self.type)

    def is_payment_notification(self) -> bool:
        """Verifica se a notificação é relacionada a pagamento."""
        if not self.has_type():
            return False
        return "payment" in str(self.type).lower()

    def is_order_notification(self) -> bool:
        """Verifica se a notificação é relacionada a pedido."""
        if not self.has_type():
            return False
        return "order" in str(self.type).lower()

    def get_payment_id(self) -> Optional[str]:
        """Extrai o ID do pagamento dos dados da notificação, se disponível."""
        if not self.is_payment_notification():
            return None
        return str(self.data.get("id", ""))

    def to_dict(self) -> dict:
        """Converte o model para dicionário."""
        return self.model_dump()
