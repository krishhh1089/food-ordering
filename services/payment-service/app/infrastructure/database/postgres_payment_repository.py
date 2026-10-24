from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.payment import Payment
from app.domain.entities.payment_status import PaymentStatus
from app.domain.repositories.payment_repository import PaymentRepository
from app.infrastructure.database.models import PaymentModel


class PostgresPaymentRepository(PaymentRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, payment: Payment) -> None:
        payment_model = PaymentModel(
            id=str(payment.payment_id),
            order_id=str(payment.order_id),
            amount=payment.amount,
            status=payment.status.value,
        )

        self.session.add(payment_model)

    def find_by_id(self, payment_id: UUID) -> Payment | None:
        payment_model = self.session.get(
            PaymentModel,
            str(payment_id),
        )

        if payment_model is None:
            return None

        return Payment.rehydrate(
            payment_id=UUID(payment_model.id),
            order_id=UUID(payment_model.order_id),
            amount=float(payment_model.amount),
            status=PaymentStatus(payment_model.status),
        )

    def find_by_order_id(self, order_id: UUID) -> Payment | None:
        payment_model = self.session.scalar(
            select(PaymentModel).where(
                PaymentModel.order_id == str(order_id)
            )
        )

        if payment_model is None:
            return None

        return Payment.rehydrate(
            payment_id=UUID(payment_model.id),
            order_id=UUID(payment_model.order_id),
            amount=float(payment_model.amount),
            status=PaymentStatus(payment_model.status),
        )