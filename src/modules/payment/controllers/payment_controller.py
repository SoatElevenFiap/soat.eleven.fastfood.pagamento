from http import HTTPMethod
from typing import Optional

from modules.payment.dtos import CreatePaymentOrderRequestDto
from modules.payment.dtos.payment_dto import PaymentDto
from modules.payment.providers import GetPaymentApplicationServiceProvider
from modules.payment.providers.create_payment_order_service import (
    CreatePaymentOrderServiceProvider,
)
from modules.shared.adapters import APIController
from modules.shared.decorators import API


@API.controller("payment", "Pagamento")
class PaymentController(APIController):
    @API.route("/", method=HTTPMethod.POST, response_model=PaymentDto)
    async def create_payment(
        self,
        request: CreatePaymentOrderRequestDto,
        create_payment_order_service: CreatePaymentOrderServiceProvider,
    ):
        return await create_payment_order_service.process(request)

    @API.route("/", method=HTTPMethod.GET, response_model=PaymentDto)
    async def get_payment(
        self,
        get_payment_application_service: GetPaymentApplicationServiceProvider,
        id: Optional[str] = None,
        end_to_end_id: Optional[str] = None,
    ):
        return await get_payment_application_service.process(
            id=id, end_to_end_id=end_to_end_id
        )
