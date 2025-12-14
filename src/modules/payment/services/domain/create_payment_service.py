from modules.external_provider.entities import ExternalOrderEntity
from modules.payment.entities import PaymentEntity
from modules.payment.enums import PaymentStatus
from modules.payment.repositories.payment_repository import PaymentRepository
from modules.shared.adapters import DomainService
from modules.shared.constants import ExceptionConstants
from modules.shared.exceptions.domain_exception import DomainException


class CreatePaymentService(DomainService):
    def __init__(self, payment_repository: PaymentRepository):
        self.__payment_repository = payment_repository
        super().__init__(context=CreatePaymentService.__name__)

    async def process(self, order: ExternalOrderEntity) -> PaymentEntity:
        existing_payment = await self.__payment_repository.get_payment_by_end_to_end_id(
            order.end_to_end_id
        )

        if existing_payment:
            self.logger.error(
                f"Payment already exists with end_to_end_id: {order.end_to_end_id}. "
            )
            raise DomainException(
                ExceptionConstants.PAYMENT_ALREADY_EXISTS,
                f"Payment already exists with end_to_end_id: {order.end_to_end_id}",
            )

        self.logger.info(
            f"Creating new payment with end_to_end_id: {order.end_to_end_id}"
        )
        entity = PaymentEntity(
            end_to_end_id=order.end_to_end_id,
            external_reference_id=order.id,
            value=order.amount,
            provider=order.provider,
            client_id=order.client_id,
            status=PaymentStatus.PENDING,
            redirect_url=order.redirect_url,
        )
        payment = await self.__payment_repository.add_payment(entity)
        self.logger.info(f"Payment created: {payment.id} :: {payment.end_to_end_id}")
        return payment
