from uuid import uuid4

from app.domain.entities.order import Order
from app.domain.entities.order_item import OrderItem
from app.infrastructure.database.database import SessionLocal
from app.infrastructure.database.postgres_order_repository import (
    PostgresOrderRepository,
)


def test_save_and_find_order():

    session = SessionLocal()

    repository = PostgresOrderRepository(session)

    order = Order(
        order_id=uuid4(),
        customer_id=uuid4(),
        restaurant_id=uuid4(),
    )

    pizza = OrderItem(
        menu_item_id=uuid4(),
        name="Pizza",
        price=250,
        quantity=2,
    )

    order.add_item(pizza)

    repository.save(order)

    saved_order = repository.find_by_id(
        order.order_id
    )

    assert saved_order is not None
    assert isinstance(saved_order, Order)

    assert saved_order.order_id == order.order_id
    assert saved_order.customer_id == order.customer_id
    assert saved_order.restaurant_id == order.restaurant_id

    assert len(saved_order.items) == 1
    assert saved_order.items[0].name == "Pizza"
    assert saved_order.items[0].quantity == 2
    assert saved_order.total() == 500

    session.close()