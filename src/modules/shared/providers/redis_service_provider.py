from typing import Annotated

from fastapi import Depends

from modules.shared.providers.settings_provider import SettingsProvider
from modules.shared.services.redis import RedisService


def redis_service_provider(settings: SettingsProvider):
    return RedisService(connection_string=settings.redis_connection_string)


RedisServiceProvider = Annotated[RedisService, Depends(redis_service_provider)]
