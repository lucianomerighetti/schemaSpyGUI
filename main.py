# main.py
import sys
from PyQt6.QtWidgets               import QApplication
from shared.components.main_window import MainWindow
from shared.themes.theme_manager   import ThemeManager

from infrastructure.database import (
    Base,
    engine
)
from modules.projects import (
    Project
)
from PyQt6.QtGui import QIcon


Base.metadata.create_all(bind=engine)

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(
        QIcon("resources/icons/schemaspygui.ico")
        )
    #app.setStyleSheet(ThemeManager.light())
    app.setStyleSheet(ThemeManager.dark())
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
