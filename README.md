# Food Ordering Services

A small food-ordering project with an order API and a payment-service Kafka
consumer. The order service stores orders in PostgreSQL and publishes an
`order-created` event; the payment service currently consumes and logs that
event.

## Services

- **Order service** — FastAPI API for creating and retrieving orders.
- **Payment service** — Kafka consumer for `order-created` events. Payment
  persistence and processing are not implemented yet.
- **Infrastructure** — Docker Compose starts PostgreSQL and Kafka.

## Requirements

- Python 3.10 or newer
- Docker Compose

## Start infrastructure

From the repository root:

```powershell
docker compose up -d
```

This starts PostgreSQL on `localhost:5432` and Kafka on `localhost:9092`.

## Run the order service

In a PowerShell terminal:

```powershell
cd services\order-service
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/food_ordering"
alembic upgrade head
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; interactive API documentation
is at `http://127.0.0.1:8000/docs`.

### API

- `POST /orders` — create an order.
- `GET /orders/{order_id}` — retrieve an order by UUID.

Example request body for `POST /orders`:

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

## Run the payment consumer

In another PowerShell terminal, with Kafka running:

```powershell
cd services\payment-service
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m app.infrastructure.messaging.kafka_event_consumer
```

The consumer listens to the `order-created` topic. Create an order while it is
running to see the event logged.

## Run order-service tests

From `services\order-service`, activate its virtual environment and run:

```powershell
python -m pytest
```
