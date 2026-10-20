from uuid import uuid4

from app.application.commands.create_order import CreateOrderCommand
from app.domain.entities.order import Order
from app.domain.repositories.order_repository import OrderRepository
from app.application.events.order_created import OrderCreatedEvent
from app.application.events.event_publisher import EventPublisher
from app.infrastructure.messaging.in_memory_event_publisher import (
    InMemoryEventPublisher,
)

event_publisher = InMemoryEventPublisher()
class CreateOrderHandler:

    def __init__(
    self,
    repository: OrderRepository,
    event_publisher: EventPublisher,
):
        self.repository = repository
        self.event_publisher = event_publisher

    def handle(self, command: CreateOrderCommand) -> Order:

        order = Order(
            order_id=uuid4(),
            customer_id=command.customer_id,
            restaurant_id=command.restaurant_id,
        )

        for item in command.items:
            order.add_item(item)

        self.repository.save(order)

        event = OrderCreatedEvent(
            order_id=order.order_id,
            customer_id=order.customer_id,
            restaurant_id=order.restaurant_id,
            total=order.total(),
        )
        
        self.event_publisher.publish(event)

        
        return order