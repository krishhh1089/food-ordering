import json

from kafka import KafkaProducer

from app.application.events.event_publisher import EventPublisher
from app.application.events.order_created import OrderCreatedEvent


class KafkaEventPublisher(EventPublisher):

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        )

    def publish(self, event) -> None:

        if isinstance(event, OrderCreatedEvent):

            message = {
                "event_type": "OrderCreated",
                "order_id": str(event.order_id),
                "customer_id": str(event.customer_id),
                "restaurant_id": str(event.restaurant_id),
                "total": event.total,
            }

            self.producer.send(
                "order-created",
                value=message,
            )

            self.producer.flush()