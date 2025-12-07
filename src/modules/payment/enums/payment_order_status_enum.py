from enum import Enum


class PaymentOrderStatus(Enum, str):
    PROCESSING = "processing"
    CREATED = "created"
    CANCELLED = "cancelled"
    SENDED_NOTIFICATION = "sended_notification"
