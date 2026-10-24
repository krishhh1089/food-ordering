import json
from datetime import datetime, timezone

from kafka import KafkaProducer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.database.models import OutboxEventModel


class OutboxPublisher:

    def __init__(self, session: Session):
        self.session = session

        self.producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )

    def publish_pending_events(self) -> None:

        events = self.session.scalars(
            select(OutboxEventModel).where(
                OutboxEventModel.published_at.is_(None)
            )
        ).all()

        for event in events:

            payload = json.loads(event.payload)

            self.producer.send(
                "order-created",
                value=payload,
            )

            self.producer.flush()

            event.published_at = datetime.now(timezone.utc)

        self.session.commit()
        
from app.infrastructure.database.database import SessionLocal


if __name__ == "__main__":
    session = SessionLocal()

    try:
        publisher = OutboxPublisher(session)
        publisher.publish_pending_events()
    finally:
        session.close()