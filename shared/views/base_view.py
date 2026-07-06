#base_view.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QLabel

class BaseView(QWidget):
    def __init__(self, title: str):
        super().__init__()
        self._main_layout = QVBoxLayout()
        self._title = QLabel(title)
        self._title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        """)

        self._main_layout.addWidget(
            self._title
        )

        self.setLayout(
            self._main_layout
        )

    @property
    def content_layout(self):
        return self._main_layout