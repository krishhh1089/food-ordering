from uuid import uuid4

from app.application.commands.create_order import CreateOrderCommand
from app.application.events.order_created import OrderCreatedEvent
from app.application.unit_of_work import UnitOfWork
from app.domain.entities.order import Order


class CreateOrderHandler:

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work

    def handle(self, command: CreateOrderCommand) -> Order:

        order = Order(
            order_id=uuid4(),
            customer_id=command.customer_id,
            restaurant_id=command.restaurant_id,
        )

        for item in command.items:
            order.add_item(item)

        # Save order
        self.unit_of_work.order_repository.save(order)

        # Create domain/application event
        event = OrderCreatedEvent(
            order_id=order.order_id,
            customer_id=order.customer_id,
            restaurant_id=order.restaurant_id,
            total=order.total(),
        )
        
        # Save event to outbox
        self.unit_of_work.outbox_repository.add_order_created_event(
            event
        )

        try:
            self.unit_of_work.commit()
        except Exception:
            self.unit_of_work.rollback()
            raise

        return order