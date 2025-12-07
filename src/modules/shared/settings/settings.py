from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: Optional[str] = None
    redis_connection_string: Optional[str] = None
    mongo_connection_string: Optional[str] = None
    mercado_pago_access_token: Optional[str] = None

    def is_development(self) -> bool:
        return self.environment == "development"

    class Config:
        env_file = ".env"
