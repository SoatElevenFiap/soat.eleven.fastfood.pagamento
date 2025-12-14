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
            if entity_class:
                try:
                    data = json.loads(cached_data)
                    if isinstance(data, list):
                        # Mapear 'id' para '_id' para compatibilidade com EntityAdapter
                        mapped_data = [
                            (
                                {**item, "_id": item.get("id")}
                                if "id" in item and "_id" not in item
                                else item
                            )
                            for item in data
                        ]
                        return (
                            [entity_class(**item) for item in mapped_data]
                            if mapped_data
                            else []
                        )
                    # Mapear 'id' para '_id' para compatibilidade com EntityAdapter
                    if "id" in data and "_id" not in data:
                        data["_id"] = data.get("id")
                    return entity_class(**data)
                except (json.JSONDecodeError, TypeError):
                    try:
                        return entity_class.model_validate_json(cached_data)
                    except Exception:
                        data = json.loads(cached_data)
                        if (
                            isinstance(data, dict)
                            and "id" in data
                            and "_id" not in data
                        ):
                            data["_id"] = data.get("id")
                        return entity_class(**data)
            return cached_data
        value = await callback()
        if value is not None:
            self.set_value(key, value, expire_in_milliseconds)
        return value
