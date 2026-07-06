#base_viewmodel.py
from __future__ import annotations
from PyQt6.QtCore import QObject
from PyQt6.QtCore import pyqtSignal

class BaseViewModel(QObject):
    # Classe base para todos os ViewModels.

    loading_changed = pyqtSignal(bool)
    error_occurred = pyqtSignal(str)
    message_emitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._loading = False

    @property
    def loading(self) -> bool:
        return self._loading

    def set_loading(self, value: bool) -> None:
        if self._loading == value:
            return
        self._loading = value
        self.loading_changed.emit(value)

    def emit_error(self, message: str) -> None:
        self.error_occurred.emit(message)

    def emit_message(self, message: str) -> None:
        self.message_emitted.emit(message)