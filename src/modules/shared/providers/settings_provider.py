from typing import Annotated

from fastapi import Depends

from modules.shared.settings.settings import Settings


def settings_provider():
    return Settings()


SettingsProvider = Annotated[Settings, Depends(settings_provider)]
