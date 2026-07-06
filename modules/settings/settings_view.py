# settings_view.py
from shared.views.base_view import BaseView

class SettingView(BaseView):

    def __init__(self):
        super().__init__("Configurações")
        self.content_layout.addStretch()