from enum import Enum


class ExternalProviderPaymentStatus(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    EXPIRED = "expired"
    ERROR = "error"
