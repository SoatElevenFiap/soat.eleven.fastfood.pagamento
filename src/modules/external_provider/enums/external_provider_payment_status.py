from enum import Enum


class ExternalProviderPaymentStatus(Enum, str):
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    EXPIRED = "expired"
    ERROR = "error"