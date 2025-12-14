PAYMENT_BASE_CACHE = "payment:"
PAYMENT_E2E_BASE_CACHE = "payment:e2e:"


class PaymentCacheKeys:
    @staticmethod
    def payment_key_for(payment_id: str) -> str:
        return PAYMENT_BASE_CACHE + payment_id

    @staticmethod
    def payment_by_end_to_end_id_key_for(end_to_end_id: str) -> str:
        return PAYMENT_E2E_BASE_CACHE + end_to_end_id
