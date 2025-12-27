from typing import Annotated, Optional

from fastapi import Depends

from modules.shared.providers.keyvault_service_provider import (
    KeyVaultServiceProvider,
)
from modules.shared.providers.settings_provider import SettingsProvider
from modules.shared.services.mongo.mongo_service import MongoService


def mongo_service_provider(
    settings: SettingsProvider, keyvault_service: KeyVaultServiceProvider
) -> MongoService:
    connection_string: Optional[str] = None

    if keyvault_service:
        connection_string = keyvault_service.get_secret("mongo-connection-string")

    if not connection_string:
        connection_string = settings.mongo_connection_string

    if not connection_string:
        raise ValueError(
            "MongoDB connection string not found in Key Vault or environment variables."
        )

    return MongoService(connection_string=connection_string)


MongoServiceProvider = Annotated[MongoService, Depends(mongo_service_provider)]
