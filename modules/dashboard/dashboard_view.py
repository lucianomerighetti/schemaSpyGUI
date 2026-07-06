# dashboard_view.py

from shared.views.base_view import BaseView

class DashboardView(BaseView):

    def __init__(self):
        super().__init__("Dashboard")
        self.content_layout.addStretch()