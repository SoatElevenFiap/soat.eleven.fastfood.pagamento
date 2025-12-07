PAYMENT_BASE_CACHE = "payment:"


class PaymentCacheKeys:
    @staticmethod
    def payment_key_for(payment_id: str) -> str:
        return PAYMENT_BASE_CACHE + payment_id

