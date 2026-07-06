# theme_manager.py

from shared.themes.dark_theme import DARK_THEME
from shared.themes.light_theme import LIGHT_THEME


class ThemeManager:

    @staticmethod
    def dark():
        return DARK_THEME

    @staticmethod
    def light():
        return LIGHT_THEME