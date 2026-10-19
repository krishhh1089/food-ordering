from uuid import UUID

from app.domain.entities.order import Order
from app.domain.repositories.order_repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):

    def __init__(self):
        self.orders: dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self.orders[str(order.order_id)] = order

    def find_by_id(self, order_id: UUID) -> Order | None:
        return self.orders.get(str(order_id))