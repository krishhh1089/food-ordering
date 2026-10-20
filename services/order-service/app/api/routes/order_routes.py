from uuid import UUID

from fastapi import APIRouter,Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.application.queries.get_order import GetOrderQuery
from app.application.handlers.get_order_handler import GetOrderHandler
from app.application.commands.create_order import CreateOrderCommand
from app.application.handlers.create_order_handler import CreateOrderHandler
from app.domain.entities.order_item import OrderItem
from app.infrastructure.database.database import get_db
from app.infrastructure.database.postgres_order_repository import (
    PostgresOrderRepository,
)

router = APIRouter()



class OrderItemRequest(BaseModel):
    menu_item_id: UUID
    name: str
    price: float
    quantity: int


class CreateOrderRequest(BaseModel):
    customer_id: UUID
    restaurant_id: UUID
    items: list[OrderItemRequest]


@router.post("/orders")
def create_order(request: CreateOrderRequest,
db: Session = Depends(get_db),):

    items = [
        OrderItem(
            menu_item_id=item.menu_item_id,
            name=item.name,
            price=item.price,
            quantity=item.quantity,
        )
        for item in request.items
    ]

    command = CreateOrderCommand(
        customer_id=request.customer_id,
        restaurant_id=request.restaurant_id,
        items=items,
    )
    repository = PostgresOrderRepository(db)
    
    handler = CreateOrderHandler(repository)

    order = handler.handle(command)

    return {
        "order_id": str(order.order_id),
        "customer_id": str(order.customer_id),
        "restaurant_id": str(order.restaurant_id),
        "status": order.status.value,
        "total": order.total(),
    }

@router.get("/orders/{order_id}")
def get_order(order_id: UUID,
    db: Session = Depends(get_db),):

    repository = PostgresOrderRepository(db)

    handler = GetOrderHandler(repository)

    query = GetOrderQuery(order_id=order_id)

    order = handler.handle(query)


    if order is None:
        return {
            "message": "Order not found"
        }

    return {
        "order_id": str(order.order_id),
        "customer_id": str(order.customer_id),
        "restaurant_id": str(order.restaurant_id),
        "status": order.status.value,
        "total": order.total(),
    }