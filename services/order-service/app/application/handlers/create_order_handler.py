from uuid import uuid4

from app.application.commands.create_order import CreateOrderCommand
from app.domain.entities.order import Order
from app.domain.repositories.order_repository import OrderRepository


class CreateOrderHandler:

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def handle(self, command: CreateOrderCommand) -> Order:

        order = Order(
            order_id=uuid4(),
            customer_id=command.customer_id,
            restaurant_id=command.restaurant_id,
        )

        for item in command.items:
            order.add_item(item)

        self.repository.save(order)

        return order