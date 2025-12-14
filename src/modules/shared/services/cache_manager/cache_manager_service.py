import json
from abc import ABC
from typing import Awaitable, Callable, List, Optional, Type, TypeVar

from pydantic import BaseModel

from modules.shared.adapters.cache_adapter import CacheAdapter

T = TypeVar("T", str, BaseModel, List[BaseModel])


class CacheManagerService(ABC):
    def __init__(self, cache: CacheAdapter):
        self.__cache = cache

    def get_value(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        return self.__cache.get_value(key, default_value)

    def set_value(
        self,
        key: str,
        value: str | BaseModel | List[BaseModel],
        expire_in_milliseconds: Optional[int] = None,
    ) -> bool:
        if isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], BaseModel):
                value = json.dumps(
                    [item.model_dump(mode="json", by_alias=True) for item in value]
                )
            elif len(value) == 0:
                value = json.dumps([])
        elif isinstance(value, BaseModel):
            value = value.model_dump_json(by_alias=True)
        return self.__cache.set_value(key, value, expire_in_milliseconds)

    def expire_keys(self, keys: List[str]) -> bool:
        return all(self.__cache.delete_value(key) for key in keys)

    def _map_id_to_underscore_id(self, data: dict) -> dict:
        """Mapeia 'id' para '_id' para compatibilidade com EntityAdapter."""
        if "id" in data and "_id" not in data:
            data["_id"] = data.get("id")
        return data

    def _deserialize_entity_list(
        self, data: List[dict], entity_class: Type[BaseModel]
    ) -> List[BaseModel]:
        """Deserializa uma lista de entidades do cache."""
        if not data:
            return []
        mapped_data = [
            (
                self._map_id_to_underscore_id(item.copy())
                if isinstance(item, dict)
                else item
            )
            for item in data
        ]
        return [entity_class(**item) for item in mapped_data]

    def _deserialize_entity(
        self, cached_data: str, entity_class: Type[BaseModel]
    ) -> BaseModel | List[BaseModel]:
        """Deserializa uma entidade do cache com fallback para diferentes formatos."""
        try:
            data = json.loads(cached_data)
            if isinstance(data, list):
                return self._deserialize_entity_list(data, entity_class)
            if isinstance(data, dict):
                mapped_data = self._map_id_to_underscore_id(data)
                return entity_class(**mapped_data)
        except (json.JSONDecodeError, TypeError):
            pass

        try:
            return entity_class.model_validate_json(cached_data)
        except Exception:
            data = json.loads(cached_data)
            if isinstance(data, dict):
                mapped_data = self._map_id_to_underscore_id(data)
                return entity_class(**mapped_data)
            raise

    def _parse_cached_entity(
        self, cached_data: str, entity_class: Optional[Type[BaseModel]]
    ) -> Optional[T]:
        """Parseia dados do cache para entidade ou retorna string."""
        if not entity_class:
            return cached_data
        return self._deserialize_entity(cached_data, entity_class)

    async def build_cache_operation(
        self,
        key: str,
        callback: Callable[[], Awaitable[T]],
        entity_class: Optional[Type[BaseModel]] = None,
        expire_in_milliseconds: Optional[int] = None,
        default_value: Optional[str] = None,
    ) -> Optional[T]:
        cached_data = self.get_value(key, default_value)
        if cached_data:
            return self._parse_cached_entity(cached_data, entity_class)

        value = await callback()
        if value is not None:
            self.set_value(key, value, expire_in_milliseconds)
        return value
