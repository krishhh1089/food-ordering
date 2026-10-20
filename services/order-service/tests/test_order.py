from uuid import uuid4

from app.application.commands.create_order import CreateOrderCommand
from app.application.handlers.create_order_handler import CreateOrderHandler
from app.domain.entities.order_item import OrderItem
from app.infrastructure.database.in_memory_order_repository import (
    InMemoryOrderRepository,
)
from app.infrastructure.messaging.in_memory_event_publisher import (
    InMemoryEventPublisher,
)

def test_create_order():

    repository = InMemoryOrderRepository()

    event_publisher = InMemoryEventPublisher()

    handler = CreateOrderHandler(
        repository,
        event_publisher,
    )

    pizza = OrderItem(
        menu_item_id=uuid4(),
        name="Pizza",
        price=250,
        quantity=2,
    )

    burger = OrderItem(
        menu_item_id=uuid4(),
        name="Burger",
        price=150,
        quantity=1,
    )

    command = CreateOrderCommand(
        customer_id=uuid4(),
        restaurant_id=uuid4(),
        items=[pizza, burger],
    )

    order = handler.handle(command)

    saved_order = repository.find_by_id(order.order_id)

    assert saved_order is not None
    assert saved_order.order_id == order.order_id

    assert len(saved_order.items) == 2

    assert saved_order.items[0].name == "Pizza"
    assert saved_order.items[0].quantity == 2

    assert saved_order.items[1].name == "Burger"
    assert saved_order.items[1].quantity == 1

    assert saved_order.total() == 650