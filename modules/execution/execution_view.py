# execution_view.py

from shared.views.base_view import BaseView

class ExecutionView(BaseView):

    def __init__(self):
        super().__init__("Execução")
        self.content_layout.addStretch()