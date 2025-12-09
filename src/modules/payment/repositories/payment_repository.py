from datetime import UTC, datetime
from typing import Optional

from modules.payment.entities import PaymentEntity
from modules.payment.enums import PaymentStatus
from modules.shared.adapters import RepositoryAdapter
from modules.shared.providers import MongoServiceProvider


class PaymentRepository(RepositoryAdapter):
    def __init__(self, mongo_service: MongoServiceProvider):
        self.__mongo_service = mongo_service
        super().__init__(table="payments")

    async def add_payment(self, payment: PaymentEntity) -> PaymentEntity:
        payment.generate_created_at()
        payment.generate_updated_at()
        payment_id = await self.__mongo_service.add_document(
            self.table, payment.model_dump(exclude=["id"])
        )
        return await self.get_payment(payment_id)

    async def make_payment_paid(self, payment_id: str) -> Optional[PaymentEntity]:
        payment_document = await self.__mongo_service.update_document(
            self.table, {"id": payment_id}, {"status": PaymentStatus.PAID, "updated_at": datetime.now(UTC)}
        )
        return PaymentEntity(**payment_document) if payment_document else None

    async def change_payment_status(
        self, payment_id: str, status: PaymentStatus
    ) -> Optional[PaymentEntity]:
        payment_document = await self.__mongo_service.update_document(
            self.table,
            {"id": payment_id},
            {"status": status, "updated_at": datetime.now(UTC)},
        )
        return PaymentEntity(**payment_document) if payment_document else None

    async def get_payment(self, payment_id: str) -> Optional[PaymentEntity]:
        payment_document = await self.__mongo_service.get_document(
            self.table, {"id": payment_id}
        )
        return PaymentEntity(**payment_document) if payment_document else None

    async def get_payment_by_end_to_end_id(
        self, end_to_end_id: str
    ) -> Optional[PaymentEntity]:
        payment_document = await self.__mongo_service.get_document(
            self.table, {"end_to_end_id": end_to_end_id}
        )
        return PaymentEntity(**payment_document) if payment_document else None
