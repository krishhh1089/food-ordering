from uuid import uuid4

from app.application.events.order_created import OrderCreatedEvent
from app.application.unit_of_work import UnitOfWork
from app.domain.entities.payment import Payment


class ProcessOrderCreatedHandler:

    def __init__(self, unit_of_work: UnitOfWork):
        self.unit_of_work = unit_of_work

    def handle(self, event: OrderCreatedEvent) -> Payment:

        # 1. Check whether we already processed this order
        existing_payment = self.unit_of_work.payment_repository.find_by_order_id(
            event.order_id
        )

        if existing_payment is not None:
            return existing_payment

        # 2. Create Payment domain entity
        payment = Payment(
            payment_id=uuid4(),
            order_id=event.order_id,
            amount=event.total,
        )

        # 3. Save Payment
        self.unit_of_work.payment_repository.save(payment)

        # 4. Create Outbox event
        self.unit_of_work.outbox_repository.add_payment_event(
            event_type="PaymentCreated",
            payload={
                "event_type": "PaymentCreated",
                "payment_id": str(payment.payment_id),
                "order_id": str(payment.order_id),
                "amount": payment.amount,
                "status": payment.status.value,
            },
        )

        # 5. Commit Payment + Outbox together
        try:
            self.unit_of_work.commit()
        except Exception:
            self.unit_of_work.rollback()
            raise

        return payment