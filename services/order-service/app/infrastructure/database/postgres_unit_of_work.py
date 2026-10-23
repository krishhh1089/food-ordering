from sqlalchemy.orm import Session

from app.application.unit_of_work import UnitOfWork
from app.infrastructure.database.outbox_repository import OutboxRepository
from app.infrastructure.database.postgres_order_repository import PostgresOrderRepository


class PostgresUnitOfWork(UnitOfWork):

    def __init__(self, session: Session):
        self.session = session

        self.order_repository = PostgresOrderRepository(
            session
        )

        self.outbox_repository = OutboxRepository(
            session
        )

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()