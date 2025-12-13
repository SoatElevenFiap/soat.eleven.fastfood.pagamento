from typing import Annotated

from fastapi import Depends

from modules.shared.services.cache_manager import CacheManagerService
from modules.shared.providers.redis_service_provider import RedisServiceProvider


def cache_manager_service_provider(
    redis_service: RedisServiceProvider,
):
    return CacheManagerService(cache=redis_service)


CacheManagerServiceProvider = Annotated[
    CacheManagerService, Depends(cache_manager_service_provider)
]
