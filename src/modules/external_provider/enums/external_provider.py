from enum import Enum


class ExternalProvider(str, Enum):
    MERCADOPAGO = "mercadopago"
    PAGSEGURO = (
        "pagseguro"  # Adicionado apenas para exemplo de provider nao implementado.
    )
