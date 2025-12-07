from http import HTTPMethod

from modules.payment.dtos import CreatePaymentOrderRequestDto
from modules.payment.entities import PaymentEntity
from modules.payment.providers.create_payment_order_service import (
    CreatePaymentOrderServiceProvider,
)
from modules.shared.adapters import APIController
from modules.shared.decorators import API
from modules.shared.providers.redis_service_provider import RedisServiceProvider


@API.controller("payment", "Pagamento")
class PaymentController(APIController):
    @API.route("/", method=HTTPMethod.POST, response_model=PaymentEntity)
    async def create_payment(
        self,
        request: CreatePaymentOrderRequestDto,
        create_payment_order_service: CreatePaymentOrderServiceProvider,
    ):
        return await create_payment_order_service.process(request)

    @API.route("/", method=HTTPMethod.GET)
    async def get_payment(
        self,
        redis_service: RedisServiceProvider,
    ):
        return redis_service.get_value("payment", "No payment found")
