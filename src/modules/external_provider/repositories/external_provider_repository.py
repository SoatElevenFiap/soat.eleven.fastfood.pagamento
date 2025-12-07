from typing import Any, Dict

from modules.shared.adapters import RepositoryAdapter
from modules.shared.providers.mongo_service_provider import MongoServiceProvider


class ExternalProviderRepository(RepositoryAdapter):
    def __init__(self, mongo_service: MongoServiceProvider):
        self.__mongo_service = mongo_service
        super().__init__(table="external_provider_requests")

    async def add_external_provider_request(self, request: Dict[str, Any]):
        await self.__mongo_service.add_document(self.table, request)
