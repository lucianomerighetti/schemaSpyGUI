# status_bar.py

from PyQt6.QtWidgets import QStatusBar


class AppStatusBar(QStatusBar):

    def __init__(self):
        super().__init__()

        self.showMessage("SchemaSpy GUI | Python: OK | API: Offline")