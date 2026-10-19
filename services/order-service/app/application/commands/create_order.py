from uuid import UUID

from app.domain.entities.order_item import OrderItem


class CreateOrderCommand:

    def __init__(
        self,
        customer_id: UUID,
        restaurant_id: UUID,
        items: list[OrderItem],
    ):
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.items = items