from typing import Any, Dict, Optional

from faker import Faker

from modules.shared.services.mercadopago.models import MercadoPagoNotificationModel


class FakerPaymentNotification:
    @staticmethod
    def create(
        payload: Optional[Dict[str, Any]] = None,
    ) -> MercadoPagoNotificationModel:
        if not payload:
            payload = {}

        faker = Faker()
        default_payload = {
            "id": faker.random_int(min=100000, max=999999),
            "action": faker.random_element(
                elements=("payment.created", "payment.updated")
            ),
            "api_version": faker.random_element(elements=("v1", "v2")),
            "data": {"id": str(faker.random_int(min=100000000, max=999999999))},
            "date_created": faker.iso8601(),
            "live_mode": faker.boolean(),
            "type": "payment",
            "user_id": faker.random_int(min=10000, max=99999),
        }
        return MercadoPagoNotificationModel(**{**default_payload, **payload})
