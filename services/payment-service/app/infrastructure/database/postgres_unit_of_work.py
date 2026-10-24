from sqlalchemy.orm import Session

from app.application.unit_of_work import UnitOfWork
from app.infrastructure.database.payment_outbox_repository import (
    PaymentOutboxRepository,
)
from app.infrastructure.database.postgres_payment_repository import (
    PostgresPaymentRepository,
)


class PostgresUnitOfWork(UnitOfWork):
    def __init__(self, session: Session):
        self.session = session

        self.payment_repository = PostgresPaymentRepository(session)
        self.outbox_repository = PaymentOutboxRepository(session)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()