from app.application.events.order_created import OrderCreatedEvent


class OrderCreatedEventHandler:

    def handle(self, event: OrderCreatedEvent) -> None:
        print("Handling OrderCreated event")
        print(f"Order ID: {event.order_id}")
        print(f"Customer ID: {event.customer_id}")
        print(f"Restaurant ID: {event.restaurant_id}")
        print(f"Total: {event.total}")