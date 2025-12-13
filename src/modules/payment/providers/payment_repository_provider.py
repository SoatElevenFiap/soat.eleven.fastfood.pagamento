from typing import Annotated

from fastapi import Depends

from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.providers import MongoServiceProvider, CacheManagerServiceProvider


def get_payment_repository_provider(
    mongo_service: MongoServiceProvider,
    cache_manager_service: CacheManagerServiceProvider,
):
    return PaymentRepository(
        mongo_service=mongo_service,
        cache_manager_service=cache_manager_service,
    )


PaymentRepositoryProvider = Annotated[
    PaymentRepository, Depends(get_payment_repository_provider)
]
