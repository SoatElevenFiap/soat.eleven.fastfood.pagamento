from typing import Annotated, Optional

from fastapi import Depends

from modules.shared.providers.settings_provider import SettingsProvider
from modules.shared.services.keyvault.keyvault_service import KeyVaultService


def keyvault_service_provider(settings: SettingsProvider) -> Optional[KeyVaultService]:
    if not settings.azure_key_vault_enabled or not settings.azure_key_vault_url:
        return None
    return KeyVaultService(vault_url=settings.azure_key_vault_url, settings=settings)


KeyVaultServiceProvider = Annotated[
    Optional[KeyVaultService], Depends(keyvault_service_provider)
]
