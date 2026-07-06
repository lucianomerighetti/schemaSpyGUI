# about_view.py

from shared.views.base_view import BaseView

class AboutView(BaseView):

    def __init__(self):
        super().__init__("Sobre")
        self.content_layout.addStretch()