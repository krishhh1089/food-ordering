from abc import ABC, abstractmethod

from app.domain.repositories.order_repository import OrderRepository


class UnitOfWork(ABC):

    order_repository: OrderRepository

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass