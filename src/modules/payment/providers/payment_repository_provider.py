from typing import Annotated

from fastapi import Depends

from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.providers import MongoServiceProvider


def get_payment_repository_provider(mongo_service: MongoServiceProvider):
    return PaymentRepository(mongo_service=mongo_service)


PaymentRepositoryProvider = Annotated[
    PaymentRepository, Depends(get_payment_repository_provider)
]
