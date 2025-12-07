from typing import Annotated

from fastapi import Depends

from modules.client.providers.get_client_service_provider import (
    GetClientServiceProvider,
)
from modules.notification.services.domain.notify_listeners_service import (
    NotifyListenersService,
)


def notify_listeners_service_provider(get_client_service: GetClientServiceProvider):
    return NotifyListenersService(
        get_client_service=get_client_service,
    )


NotifyListenersServiceProvider = Annotated[
    NotifyListenersService, Depends(notify_listeners_service_provider)
]
