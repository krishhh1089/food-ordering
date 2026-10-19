from uuid import UUID
from app.domain.entities.order_status import OrderStatus

class OrderItem:

    def __init__(
        self,
        menu_item_id: UUID,
        name: str,
        price: float,
        quantity: int,
    ):
        if price < 0:
            raise ValueError("Price cannot be negative")

        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        self.menu_item_id = menu_item_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def total(self) -> float:
        return self.price * self.quantity