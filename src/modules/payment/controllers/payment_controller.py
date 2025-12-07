from http import HTTPMethod

from fastapi import HTTPException

from modules.payment.dtos import CreatePaymentOrderRequestDto
from modules.payment.entities import PaymentEntity
from modules.payment.providers.create_payment_order_service import (
    CreatePaymentOrderServiceProvider,
)
from modules.payment.providers.get_payment_service_provider import (
    GetPaymentServiceProvider,
)
from modules.shared.adapters import APIController
from modules.shared.decorators import API


@API.controller("payment", "Pagamento")
class PaymentController(APIController):
    @API.route("/", method=HTTPMethod.POST, response_model=PaymentEntity)
    async def create_payment(
        self,
        request: CreatePaymentOrderRequestDto,
        create_payment_order_service: CreatePaymentOrderServiceProvider,
    ):
        return await create_payment_order_service.process(request)

    @API.route("/", method=HTTPMethod.GET, response_model=PaymentEntity)
    async def get_payment(
        self,
        id: str,
        get_payment_service: GetPaymentServiceProvider,
    ):
        payment = await get_payment_service.process(id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
