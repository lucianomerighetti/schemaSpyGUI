from abc import ABC, abstractmethod

from .event import Event

class EventHandler(ABC):

    @abstractmethod
    def handle(self, event: Event) -> None:
        pass