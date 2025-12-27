from typing import Annotated, Optional

from fastapi import Depends

from modules.shared.providers.keyvault_service_provider import (
    KeyVaultServiceProvider,
)
from modules.shared.providers.settings_provider import SettingsProvider
from modules.shared.services.redis import RedisService


def redis_service_provider(
    settings: SettingsProvider, keyvault_service: KeyVaultServiceProvider
) -> RedisService:
    connection_string: Optional[str] = None

    if keyvault_service:
        connection_string = keyvault_service.get_secret("redis-connection-string")

    if not connection_string:
        connection_string = settings.redis_connection_string

    if not connection_string:
        raise ValueError(
            "Redis connection string not found in Key Vault or environment variables."
        )

    return RedisService(connection_string=connection_string)


RedisServiceProvider = Annotated[RedisService, Depends(redis_service_provider)]
