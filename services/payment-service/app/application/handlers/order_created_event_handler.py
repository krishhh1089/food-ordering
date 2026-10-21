from app.application.events.order_created import OrderCreatedEvent
from app.domain.entities.payment import Payment
from app.domain.repositories.payment_repository import PaymentRepository

from uuid import uuid4


class OrderCreatedEventHandler:

    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    def handle(self, event: OrderCreatedEvent) -> Payment:

        payment = Payment(
            payment_id=uuid4(),
            order_id=event.order_id,
            amount=event.total,
        )

        self.repository.save(payment)

        return payment