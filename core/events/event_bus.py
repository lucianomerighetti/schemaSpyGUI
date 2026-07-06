from __future__ import annotations
from collections import defaultdict
from typing import Any
from typing import Callable


class EventBus:
    """
    Event Bus global da aplicação.

    Permite comunicação desacoplada entre:
    - Views
    - ViewModels
    - Services
    """
    def __init__(self):
        self._subscribers = defaultdict(list)

    def subscribe(
        self,
        event_name: str,
        callback: Callable[[Any], None]
    ) -> None:
        """
        Registra um listener.
        """
        self._subscribers[event_name].append(
            callback
        )

    def unsubscribe(
        self,
        event_name: str,
        callback: Callable[[Any], None]
    ) -> None:
        """
        Remove listener.
        """
        if callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(
                callback
            )

    def publish(
        self,
        event_name: str,
        data: Any = None
    ) -> None:
        """
        Dispara evento.
        """
        for callback in self._subscribers[event_name]:
            callback(data)

    def clear(self) -> None:
        """
        Remove todos os eventos registrados.
        """
        self._subscribers.clear()