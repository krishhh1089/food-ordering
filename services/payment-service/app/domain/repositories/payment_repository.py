from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.payment import Payment


class PaymentRepository(ABC):

    @abstractmethod
    def save(self, payment: Payment) -> None:
        pass

    @abstractmethod
    def find_by_id(self, payment_id: UUID) -> Payment | None:
        pass

    @abstractmethod
    def find_by_order_id(self, order_id: UUID) -> Payment | None:
        pass