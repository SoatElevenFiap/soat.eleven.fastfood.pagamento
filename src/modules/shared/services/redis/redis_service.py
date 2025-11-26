from typing import Optional

import redis

from modules.shared.adapters.cache_adapter import CacheAdapter
from modules.shared.services.logger.logger_service import LoggerService


class RedisService(CacheAdapter):
    def __init__(self, connection_string: str) -> None:
        self.__connection_string = connection_string
        self.__client: Optional[redis.Redis] = None
        self.__logger = LoggerService("RedisService")

    def __get_client(self) -> redis.Redis:
        if self.__client is None:
            self.__client = redis.Redis.from_url(self.__connection_string)
        self.__client.ping()
        return self.__client

    def get_value(self, key: str, default_value: Optional[str] = None) -> Optional[str]:
        try:
            client = self.__get_client()
            self.__logger.info(
                f"Getting value from cache for key: <yellow>{key}</yellow>."
            )
            value = client.get(key)
            if value is None:
                return default_value
            return value.decode("utf-8") if isinstance(value, bytes) else value
        except Exception as e:
            self.__logger.error(
                f"Error getting value for key: <yellow>{key}</yellow>: <red>{e}</red>."
            )
            return default_value

    def set_value(
        self, key: str, value: str, expire_in_milliseconds: Optional[int] = None
    ) -> bool:
        try:
            client = self.__get_client()
            if client is None:
                self.__logger.error(
                    f"Error getting client for key: <yellow>{key}</yellow>."
                )
                return False

            if expire_in_milliseconds:
                expire_seconds = expire_in_milliseconds // 1000
                self.__logger.info(
                    f"Setting value in cache for key: <yellow>{key}</yellow> with expire: <yellow>{expire_seconds}</yellow> seconds."
                )
                client.setex(key, expire_seconds, value)
            else:
                self.__logger.info(
                    f"Setting value in cache for key: <yellow>{key}</yellow> without expire."
                )
                client.set(key, value)
            return True
        except Exception as e:
            self.__logger.error(
                f"Error setting value for key: <yellow>{key}</yellow>: <red>{e}</red>."
            )
            return False

    def delete_value(self, key: str) -> bool:
        try:
            client = self.__get_client()
            if client is None:
                self.__logger.error(
                    f"Error getting client for key: <yellow>{key}</yellow>."
                )
                return False

            self.__logger.info(
                f"Deleting value from cache for key: <yellow>{key}</yellow>."
            )
            result = client.delete(key)
            return bool(result)
        except Exception as e:
            self.__logger.error(
                f"Error deleting value for key: <yellow>{key}</yellow>: <red>{e}</red>."
            )
            return False
