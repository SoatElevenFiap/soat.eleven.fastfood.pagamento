import uuid
from hashlib import sha256
from http import HTTPMethod

from modules.shared.adapters import APIController
from modules.shared.decorators import API
from modules.shared.providers.redis_service_provider import RedisServiceProvider


@API.controller("payment")
class PaymentController(APIController):
    ## TESTES NO REDIS PROVISÓRIOS!

    @API.route("/", method=HTTPMethod.POST)
    async def create_payment(
        self,
        redis_service: RedisServiceProvider,
    ):
        payment_id = sha256(uuid.uuid4().hex.encode()).hexdigest()
        redis_service.set_value("payment", payment_id)
        return payment_id

    @API.route("/", method=HTTPMethod.GET)
    async def get_payment(
        self,
        redis_service: RedisServiceProvider,
    ):
        return redis_service.get_value("payment", "No payment found")
