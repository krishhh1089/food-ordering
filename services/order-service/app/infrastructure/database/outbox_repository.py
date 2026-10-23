import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.application.events.order_created import OrderCreatedEvent
from app.infrastructure.database.models import OutboxEventModel


class OutboxRepository:

    def __init__(self, session: Session):
        self.session = session

    def add_order_created_event(
        self,
        event: OrderCreatedEvent,
    ) -> None:

        event_model = OutboxEventModel(
            event_type="OrderCreated",
            payload=json.dumps(
                {
                    "event_type": "OrderCreated",
                    "order_id": str(event.order_id),
                    "customer_id": str(event.customer_id),
                    "restaurant_id": str(event.restaurant_id),
                    "total": event.total,
                }
            ),
            created_at=datetime.now(timezone.utc),
            published_at=None,
        )

        self.session.add(event_model)