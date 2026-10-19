from uuid import UUID


class GetOrderQuery:

    def __init__(self, order_id: UUID):
        self.order_id = order_id