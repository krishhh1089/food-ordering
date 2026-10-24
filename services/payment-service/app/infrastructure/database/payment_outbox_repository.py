import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.infrastructure.database.models import OutboxEventModel


class PaymentOutboxRepository:

    def __init__(self, session: Session):
        self.session = session

    def add_payment_event(
        self,
        event_type: str,
        payload: dict,
    ) -> None:

        event = OutboxEventModel(
            event_type=event_type,
            payload=json.dumps(payload),
            created_at=datetime.now(timezone.utc),
            published_at=None,
        )

        self.session.add(event)