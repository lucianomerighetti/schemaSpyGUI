# navigation_service.py

from PyQt6.QtWidgets import QStackedWidget

class NavigationService:

    def __init__(self, stack: QStackedWidget):
        self._stack = stack
        self._pages = {}

    def register_page(self, name: str, widget):
        self._pages[name] = widget
        self._stack.addWidget(widget)

    def navigate(self, name: str):
        if name not in self._pages:
            raise ValueError(
                f"Página '{name}' não registrada."
            )
        self._stack.setCurrentWidget(self._pages[name])

    def current_page(self):
        return self._stack.currentWidget()