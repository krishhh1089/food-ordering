from app.application.events.event_publisher import EventPublisher


class InMemoryEventPublisher(EventPublisher):

    def __init__(self):
        self.events = []

    def publish(self, event) -> None:
        self.events.append(event)