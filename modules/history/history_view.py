# history_view.py

from shared.views.base_view import BaseView

class HistoryView(BaseView):

    def __init__(self):
        super().__init__("Histórico")
        self.content_layout.addStretch()