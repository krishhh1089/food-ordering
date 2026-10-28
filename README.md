# Food Ordering

This repository contains a small event-driven food ordering system built with
Python services. The order service exposes a FastAPI API, persists orders in
PostgreSQL, and publishes an `order-created` event to Kafka. The payment service
listens for that event and processes it.

## Architecture

- Order service: FastAPI API for creating and retrieving orders.
- Payment service: Kafka consumer that handles `order-created` events.
- PostgreSQL: stores order and payment data.
- Kafka: event broker for asynchronous communication between services.
- Docker Compose: launches the infrastructure dependencies.

## Repository structure

```text
.
├── docker-compose.yml
├── infrastructure/
├── k8s/
├── services/
│   ├── order-service/
│   └── payment-service/
└── README.md
```

## Prerequisites

- Python 3.10+
- Docker Compose
- PowerShell (recommended for Windows setup)

## Start infrastructure

From the repository root, start PostgreSQL and Kafka:

```powershell
docker compose up -d
```

The services will be available at:

- PostgreSQL: `localhost:5432`
- Kafka: `localhost:9092`

## Run the order service

Open a PowerShell terminal and run:

```powershell
cd services\order-service
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/food_ordering"
alembic upgrade head
uvicorn app.main:app --reload
```

Once the service is running:

- API base URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

### API

- `POST /orders` — create a new order.
- `GET /orders/{order_id}` — fetch an order by UUID.

Example payload for `POST /orders`:

```json
{
  "customer_id": "00000000-0000-0000-0000-000000000001",
  "restaurant_id": "00000000-0000-0000-0000-000000000002",
  "items": [
    {
      "menu_item_id": "00000000-0000-0000-0000-000000000003",
      "name": "Sample item",
      "price": 12.5,
      "quantity": 2
    }
  ]
}
```

## Run the payment service

Open a second PowerShell terminal and run:

```powershell
cd services\payment-service
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m app.infrastructure.messaging.kafka_event_consumer
```

The consumer listens to the `order-created` topic. When you create an order via
the API, the event will be published to Kafka and processed by the payment
service.

## Run tests

From `services\order-service`:

```powershell
python -m pytest
```

## Notes

This project is a lightweight example of a microservice architecture. The order
service is the main API entry point, while Kafka is used for async event-driven
communication between services.

