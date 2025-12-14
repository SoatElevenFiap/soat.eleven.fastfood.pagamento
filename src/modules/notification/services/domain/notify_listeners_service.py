import requests

from modules.client.services.domain.get_client_service import GetClientService
from modules.payment.entities.payment_entity import PaymentEntity
from modules.shared.adapters import DomainService
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException


class NotifyListenersService(DomainService):
    def __init__(self, get_client_service: GetClientService):
        self.__get_client_service = get_client_service
        super().__init__(context=NotifyListenersService.__name__)

    async def process(self, payment: PaymentEntity):
        self.logger.info("Notifying listeners...")
        try:
            client = await self.__get_client_service.process(payment.client_id)
            if not client:
                self.logger.error(f"Client not found: {payment.client_id}")
                raise DomainException(
                    ExceptionConstants.INVALID_CLIENT,
                    f"Client not found: {payment.client_id}",
                )
            self.logger.title_box_warning(
                f"Notifying external client: {client.notification_url}"
            )
            requests.post(
                client.notification_url,
                json=payment.model_dump(mode="json"),
            )
        except Exception as e:
            self.logger.error(f"Error notifying listeners: {e}")
