from typing import Optional

from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from modules.shared.services.logger.logger_service import LoggerService
from modules.shared.settings.settings import Settings


class KeyVaultService:
    def __init__(
        self, vault_url: Optional[str] = None, settings: Optional[Settings] = None
    ) -> None:
        self.__vault_url = vault_url
        self.__settings = settings
        self.__client: Optional[SecretClient] = None
        self.__logger = LoggerService("KeyVaultService")

    def __get_client(self) -> Optional[SecretClient]:
        if not self.__vault_url:
            self.__logger.warning(
                "Key Vault URL not configured. Key Vault is disabled."
            )
            return None

        if self.__client is None:
            try:
                credential = DefaultAzureCredential()
                self.__client = SecretClient(
                    vault_url=self.__vault_url, credential=credential
                )
                self.__logger.info(
                    f"Key Vault client initialized for vault: <yellow>{self.__vault_url}</yellow>."
                )
            except Exception as e:
                self.__logger.error(
                    f"Error initializing Key Vault client: <red>{e}</red>."
                )
                return None

        return self.__client

    def get_secret(self, secret_name: str) -> Optional[str]:
        if self.__settings and self.__settings.is_development():
            self.__logger.info(
                f"Development environment detected. Skipping Key Vault and using environment variables for secret: <yellow>{secret_name}</yellow>."
            )
            return None

        if not self.__vault_url:
            return None

        try:
            client = self.__get_client()
            if client is None:
                return None

            self.__logger.info(
                f"Retrieving secret from Key Vault: <yellow>{secret_name}</yellow>."
            )
            secret = client.get_secret(secret_name)
            return secret.value
        except AzureError as e:
            self.__logger.error(
                f"Error retrieving secret <yellow>{secret_name}</yellow> from Key Vault: <red>{e}</red>."
            )
            return None
        except Exception as e:
            self.__logger.error(
                f"Unexpected error retrieving secret <yellow>{secret_name}</yellow>: <red>{e}</red>."
            )
            return None
