from typing import Optional

from faker import Faker
from modules.client.entities.client_entity import ClientEntity


class FakerClient:
    @staticmethod
    def create(payload: Optional[dict[str, any]] = None) -> ClientEntity:
        if not payload:
            payload = {}

        faker = Faker()
        default_payload = {
            "_id": faker.uuid4(),
            "name": faker.name(),
            "notification_url": faker.url(),
        }
        return ClientEntity(**{**default_payload, **payload})
