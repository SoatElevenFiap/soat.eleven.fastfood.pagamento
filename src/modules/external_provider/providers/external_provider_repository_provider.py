from typing import Annotated

from fastapi import Depends

from modules.external_provider.repositories.external_provider_repository import (
    ExternalProviderRepository,
)
from modules.shared.providers.mongo_service_provider import MongoServiceProvider


def external_provider_repository_provider(mongo_service: MongoServiceProvider):
    return ExternalProviderRepository(mongo_service=mongo_service)


ExternalProviderRepositoryProvider = Annotated[
    ExternalProviderRepository, Depends(external_provider_repository_provider)
]
