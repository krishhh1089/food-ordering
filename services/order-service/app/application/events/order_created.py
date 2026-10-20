from uuid import UUID


class OrderCreatedEvent:

    def __init__(
        self,
        order_id: UUID,
        customer_id: UUID,
        restaurant_id: UUID,
        total: float,
    ):
        self.order_id = order_id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.total = total