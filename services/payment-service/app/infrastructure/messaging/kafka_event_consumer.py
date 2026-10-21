import json
from uuid import UUID

from kafka import KafkaConsumer

from app.application.events.order_created import OrderCreatedEvent


consumer = KafkaConsumer(
    "order-created",
    bootstrap_servers="localhost:9092",
    group_id="payment-service-group",
    auto_offset_reset="earliest",
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
)

print("Payment Service Kafka consumer started...")


for message in consumer:
    data = message.value

    event = OrderCreatedEvent(
        order_id=UUID(data["order_id"]),
        customer_id=UUID(data["customer_id"]),
        restaurant_id=UUID(data["restaurant_id"]),
        total=data["total"],
    )

    print("Payment Service received OrderCreated")
    print(f"Order ID: {event.order_id}")
    print(f"Amount to pay: {event.total}")