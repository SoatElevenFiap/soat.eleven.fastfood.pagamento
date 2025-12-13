from datetime import UTC, datetime
from typing import Optional

from modules.payment.constants import PaymentCacheKeys
from modules.payment.entities import PaymentEntity
from modules.payment.enums import PaymentStatus
from modules.shared.adapters import RepositoryAdapter
from modules.shared.providers import MongoServiceProvider
from modules.shared.services.cache_manager import CacheManagerService


class PaymentRepository(RepositoryAdapter):
    def __init__(
        self,
        mongo_service: MongoServiceProvider,
        cache_manager_service: CacheManagerService,
    ):
        self.__mongo_service = mongo_service
        self.__cache_manager_service = cache_manager_service
        super().__init__(table="payments")

    async def add_payment(self, payment: PaymentEntity) -> PaymentEntity:
        payment.generate_created_at()
        payment.generate_updated_at()
        payment_id = await self.__mongo_service.add_document(
            self.table, payment.model_dump(exclude=["id"])
        )
        created_payment = await self.get_payment(payment_id)
        if created_payment:
            # Atualizar cache após criar
            self.__cache_manager_service.set_value(
                PaymentCacheKeys.payment_key_for(created_payment.id),
                created_payment,
            )
            self.__cache_manager_service.set_value(
                PaymentCacheKeys.payment_by_end_to_end_id_key_for(
                    created_payment.end_to_end_id
                ),
                created_payment,
            )
        return created_payment

    async def make_payment_paid(self, payment_id: str) -> Optional[PaymentEntity]:
        payment_document = await self.__mongo_service.update_document(
            self.table, {"id": payment_id}, {"status": PaymentStatus.PAID, "updated_at": datetime.now(UTC)}
        )
        updated_payment = PaymentEntity(**payment_document) if payment_document else None
        if updated_payment:
            # Atualizar cache após mudança de status
            self.__update_payment_cache(updated_payment)
        return updated_payment

    async def change_payment_status(
        self, payment_id: str, status: PaymentStatus
    ) -> Optional[PaymentEntity]:
        payment_document = await self.__mongo_service.update_document(
            self.table,
            {"id": payment_id},
            {"status": status, "updated_at": datetime.now(UTC)},
        )
        updated_payment = PaymentEntity(**payment_document) if payment_document else None
        if updated_payment:
            # Atualizar cache após mudança de status
            self.__update_payment_cache(updated_payment)
        return updated_payment

    async def get_payment(self, payment_id: str) -> Optional[PaymentEntity]:
        return await self.__cache_manager_service.build_cache_operation(
            key=PaymentCacheKeys.payment_key_for(payment_id),
            callback=lambda: self.__get_payment_from_db(payment_id),
            entity_class=PaymentEntity,
        )

    async def get_payment_by_end_to_end_id(
        self, end_to_end_id: str
    ) -> Optional[PaymentEntity]:
        return await self.__cache_manager_service.build_cache_operation(
            key=PaymentCacheKeys.payment_by_end_to_end_id_key_for(end_to_end_id),
            callback=lambda: self.__get_payment_by_end_to_end_id_from_db(end_to_end_id),
            entity_class=PaymentEntity,
        )

    async def __get_payment_from_db(self, payment_id: str) -> Optional[PaymentEntity]:
        payment_document = await self.__mongo_service.get_document(
            self.table, {"id": payment_id}
        )
        return PaymentEntity(**payment_document) if payment_document else None

    async def __get_payment_by_end_to_end_id_from_db(
        self, end_to_end_id: str
    ) -> Optional[PaymentEntity]:
        payment_document = await self.__mongo_service.get_document(
            self.table, {"end_to_end_id": end_to_end_id}
        )
        payment = PaymentEntity(**payment_document) if payment_document else None
        if payment:
            # Também atualizar cache pela chave de ID quando buscar por end_to_end_id
            self.__cache_manager_service.set_value(
                PaymentCacheKeys.payment_key_for(payment.id),
                payment,
            )
        return payment

    def __update_payment_cache(self, payment: PaymentEntity):
        """Atualiza ambas as chaves de cache quando o pagamento é modificado"""
        self.__cache_manager_service.set_value(
            PaymentCacheKeys.payment_key_for(payment.id),
            payment,
        )
        self.__cache_manager_service.set_value(
            PaymentCacheKeys.payment_by_end_to_end_id_key_for(payment.end_to_end_id),
            payment,
        )
