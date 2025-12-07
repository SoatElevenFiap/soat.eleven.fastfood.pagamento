from pydantic import BaseModel


class PaymentNotificationDataclass(BaseModel):
    id: int
    action: str
    api_version: str
    data: dict
    date_created: str
    live_mode: bool
    type: str
    user_id: int
