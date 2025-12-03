from typing import Annotated

from fastapi import Depends

from modules.shared.providers.settings_provider import SettingsProvider
from modules.shared.services.mongo.mongo_service import MongoService


def mongo_service_provider(settings: SettingsProvider):
    return MongoService(connection_string=settings.mongo_connection_string)


MongoServiceProvider = Annotated[MongoService, Depends(mongo_service_provider)]
