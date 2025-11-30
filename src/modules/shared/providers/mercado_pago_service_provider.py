from typing import Annotated

from fastapi import Depends

from modules.shared.services.mercadopago.mercado_pago_service import MercadoPagoService


def mercado_pago_service_provider():
    return MercadoPagoService()


MercadoPagoServiceProvider = Annotated[
    MercadoPagoService, Depends(mercado_pago_service_provider)
]
