from enum import Enum
from uuid import UUID

from app.domain.entities.order_item import OrderItem


class OrderStatus(Enum):

    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Order:

    def __init__(
        self,
        order_id: UUID,
        customer_id: UUID,
        restaurant_id: UUID,
    ):
        self.order_id = order_id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id

        self.items: list[OrderItem] = []
        self.status = OrderStatus.CREATED

    def add_item(self, item: OrderItem) -> None:

        if self.status != OrderStatus.CREATED:
            raise ValueError(
                "Cannot add items to this order"
            )

        self.items.append(item)

    def total(self) -> float:

        return sum(
            item.total()
            for item in self.items
        )

    def confirm(self) -> None:

        if not self.items:
            raise ValueError(
                "Cannot confirm an empty order"
            )

        if self.status != OrderStatus.CREATED:
            raise ValueError(
                "Only a created order can be confirmed"
            )

        self.status = OrderStatus.CONFIRMED

    def cancel(self) -> None:

        if self.status in [
            OrderStatus.PREPARING,
            OrderStatus.READY,
            OrderStatus.DELIVERED,
        ]:
            raise ValueError(
                "Order cannot be cancelled at this stage"
            )

        self.status = OrderStatus.CANCELLED
        