from abc import ABC, abstractmethod

from app.domain.repositories.payment_repository import PaymentRepository


class UnitOfWork(ABC):

    payment_repository: PaymentRepository

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass