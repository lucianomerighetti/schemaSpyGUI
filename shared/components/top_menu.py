# top_menu.py

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QHBoxLayout


class TopMenu(QWidget):

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        #title = QLabel("SchemaSpy GUI")
        #title.setStyleSheet("""
        #    font-size:16px;
        #    font-weight:bold;
        #""")
        #layout.addWidget(title)

        layout.addStretch()

        self.setLayout(layout)
        self.setFixedHeight(60)