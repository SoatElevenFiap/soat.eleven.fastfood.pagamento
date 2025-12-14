from enum import Enum

from modules.payment.enums import PaymentStatus


class MercadoPagoPaymentStatus(str, Enum):
    PENDING = "pending"  # O usuário ainda não concluiu o processo de pagamento (por exemplo, após gerar um boleto, o pagamento será concluído quando o usuário pagar no local selecionado).
    APPROVED = "approved"  # O pagamento foi aprovado e creditado com sucesso.
    AUTHORIZED = (
        "authorized"  # O pagamento foi autorizado, mas ainda não foi capturado.
    )
    IN_PROCESS = "in_process"  # O pagamento está em análise.
    IN_MEDIATION = "in_mediation"  # O usuário iniciou uma disputa.
    REJECTED = (
        "rejected"  # O pagamento foi rejeitado (o usuário pode tentar pagar novamente).
    )
    CANCELLED = "cancelled"  # O pagamento foi cancelado por uma das partes ou expirou.
    REFUNDED = "refunded"  # O pagamento foi reembolsado ao usuário.
    CHARGED_BACK = (
        "charged_back"  # Um chargeback foi aplicado no cartão de crédito do comprador.
    )

    @staticmethod
    def to_payment_status(status: str) -> PaymentStatus:
        match status:
            case MercadoPagoPaymentStatus.PENDING:
                return PaymentStatus.PENDING
            case MercadoPagoPaymentStatus.APPROVED:
                return PaymentStatus.PAID
            case MercadoPagoPaymentStatus.AUTHORIZED:
                return PaymentStatus.PENDING
            case MercadoPagoPaymentStatus.IN_PROCESS:
                return PaymentStatus.PENDING
            case MercadoPagoPaymentStatus.IN_MEDIATION:
                return PaymentStatus.REFUND_REQUESTED
            case MercadoPagoPaymentStatus.REJECTED:
                return PaymentStatus.FAILED
            case MercadoPagoPaymentStatus.CANCELLED:
                return PaymentStatus.CANCELLED
            case MercadoPagoPaymentStatus.REFUNDED:
                return PaymentStatus.REFUNDED
            case MercadoPagoPaymentStatus.CHARGED_BACK:
                return PaymentStatus.REFUNDED
            case _:
                return PaymentStatus.ERROR
