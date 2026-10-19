from uuid import UUID

from sqlalchemy.orm import Session

from app.domain.entities.order import Order
from app.domain.entities.order import OrderStatus
from app.domain.entities.order_item import OrderItem
from app.domain.repositories.order_repository import OrderRepository
from app.infrastructure.database.models import OrderModel, OrderItemModel


class PostgresOrderRepository(OrderRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, order: Order) -> None:

        order_model = OrderModel(
            id=str(order.order_id),
            customer_id=str(order.customer_id),
            restaurant_id=str(order.restaurant_id),
            status=order.status.value,
        )

        for item in order.items:

            item_model = OrderItemModel(
                menu_item_id=str(item.menu_item_id),
                name=item.name,
                price=item.price,
                quantity=item.quantity,
            )

            order_model.items.append(item_model)

        self.session.add(order_model)

        self.session.commit()

    def find_by_id(self, order_id: UUID) -> Order | None:

        order_model = self.session.get(
            OrderModel,
            str(order_id),
        )

        if order_model is None:
            return None
        
        items = [
            OrderItem(
                menu_item_id=UUID(item.menu_item_id),
                name=item.name,
                price=item.price,
                quantity=item.quantity,
            )
            for item in order_model.items
        ]

        return Order.rehydrate(
            order_id=UUID(order_model.id),
            customer_id=UUID(order_model.customer_id),
            restaurant_id=UUID(order_model.restaurant_id),
            status=OrderStatus(order_model.status),
            items=items,
        )