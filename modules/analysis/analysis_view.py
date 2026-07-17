# analysis_view.py

from shared.views.base_view import BaseView

class AnalysisView(BaseView):

    def __init__(self):
        super().__init__("Análise")
        self.content_layout.addStretch()