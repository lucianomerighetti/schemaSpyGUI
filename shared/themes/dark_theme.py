# dark_theme.py

DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    color: #ffffff;
    background-color: #1e1e1e;
    font-family: Segoe UI;
    font-size: 10pt;
}

QFrame {
    background-color: #252526;
}

QPushButton {
    background-color: #2d2d30;
    border: none;
    padding: 8px;
    text-align: center;
}

SideBar QPushButton {
    text-align: left;
}

QPushButton:hover {
    background-color: #3e3e42;
}

QStatusBar {
    background-color: #2d2d30;
}

/* --------------------------------------------------
   Grid Table
-------------------------------------------------- */

QTableWidget {
    background-color: #2B2B2B;
    alternate-background-color: #353535;
    gridline-color: #505050;
}

QTableWidget::item:selected {
    background-color: #3D5A80;
    color: #FFFFFF;
}

QTableWidget::item:selected:active {
    background-color: #4A6FA5;
    color: #FFFFFF;
}

QTableWidget::item:hover {
    background-color: #4A6FA5;
    color: #FFFFFF;
}

/* --------------------------------------------------
   Tab Widget & Tab Bar
-------------------------------------------------- */
QTabWidget::pane {
    border: 1px solid #2d2d30;
    background-color: #1e1e1e;
}

QTabBar::tab {
    background-color: #2d2d30;
    color: #ffffff;
    padding: 8px 16px;
}

QTabBar::tab:selected {
    background-color: #1e1e1e;
    color: #ffffff;
}
"""