from typing import Annotated

from fastapi import Depends

from modules.client.repositories.client_repository import ClientRepository
from modules.shared.providers import CacheManagerServiceProvider, MongoServiceProvider


def client_repository_provider(
    mongo_service: MongoServiceProvider,
    cache_manager_service: CacheManagerServiceProvider,
):
    return ClientRepository(
        mongo_service=mongo_service,
        cache_manager_service=cache_manager_service,
    )


ClientRepositoryProvider = Annotated[
    ClientRepository, Depends(client_repository_provider)
]
