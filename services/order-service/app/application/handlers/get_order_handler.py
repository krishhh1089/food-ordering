from uuid import UUID

from app.application.queries.get_order import GetOrderQuery
from app.domain.entities.order import Order
from app.domain.repositories.order_repository import OrderRepository


class GetOrderHandler:

    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def handle(self, query: GetOrderQuery) -> Order | None:

        return self.repository.find_by_id(query.order_id)