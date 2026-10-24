import json
from uuid import UUID

from kafka import KafkaConsumer

from app.application.events.order_created import OrderCreatedEvent
from app.application.handlers.process_order_created_handler import (
    ProcessOrderCreatedHandler,
)
from app.infrastructure.database.database import SessionLocal
from app.infrastructure.database.postgres_payment_repository import (
    PostgresPaymentRepository,
)
from app.infrastructure.database.postgres_unit_of_work import PostgresUnitOfWork


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

    session = SessionLocal()

    try:
        unit_of_work = PostgresUnitOfWork(session)
        handler = ProcessOrderCreatedHandler(unit_of_work)

        payment = handler.handle(event)

        print("Payment created/received")
        print(f"Payment ID: {payment.payment_id}")
        print(f"Order ID: {payment.order_id}")
        print(f"Amount: {payment.amount}")
        print(f"Status: {payment.status.value}")

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()