from __future__ import annotations
from collections import defaultdict
from typing import Any
from typing import Callable
from .event import Event


class EventBus:
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[[Any], None]) -> None:
        self._subscribers[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable[[Any], None]) -> None:
        if callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)

    def publish(self, event_name: str, data: Any = None) -> None:
        for callback in self._subscribers[event_name]:
            callback(data)

    def publish_event(self, event: Event):
        for callback in self._subscribers[event.name]:
            callback(event)

    def clear(self) -> None:
        self._subscribers.clear()
