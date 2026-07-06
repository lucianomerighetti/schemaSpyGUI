# light_theme.py

LIGHT_THEME = """
/* --------------------------------------------------
   Main Window
-------------------------------------------------- */

QMainWindow {
    background-color: #f5f5f5;
}


/* --------------------------------------------------
   Widgets
-------------------------------------------------- */

QWidget {
    background-color: #f5f5f5;
    color: #202020;
    font-family: "Segoe UI";
    font-size: 10pt;
}


/* --------------------------------------------------
   Frames
-------------------------------------------------- */

QFrame {
    background-color: #ffffff;
    border: none;
}


/* --------------------------------------------------
   Labels
-------------------------------------------------- */

QLabel {
    color: #202020;
}


/* --------------------------------------------------
   Push Buttons
-------------------------------------------------- */

QPushButton {
    background-color: #ffffff;
    color: #202020;

    border: 1px solid #d0d0d0;

    padding: 8px;
    text-align: left;

    border-radius: 4px;
}

QPushButton:hover {
    background-color: #e8e8e8;
}

QPushButton:pressed {
    background-color: #dcdcdc;
}

QPushButton:checked {
    background-color: #0078d7;
    color: white;
    border: none;
}


/* --------------------------------------------------
   Line Edit
-------------------------------------------------- */

QLineEdit {
    background-color: #ffffff;
    color: #202020;

    border: 1px solid #c0c0c0;
    border-radius: 4px;

    padding: 6px;
}


/* --------------------------------------------------
   ComboBox
-------------------------------------------------- */

QComboBox {
    background-color: #ffffff;
    color: #202020;

    border: 1px solid #c0c0c0;
    border-radius: 4px;

    padding: 6px;
}

QComboBox::drop-down {
    border: none;
}


/* --------------------------------------------------
   Table Widget
-------------------------------------------------- */

QTableWidget {
    background-color: #ffffff;
    color: #202020;

    border: 1px solid #d0d0d0;

    gridline-color: #e0e0e0;
}

QHeaderView::section {
    background-color: #ececec;
    color: #202020;

    padding: 6px;
    border: none;

    font-weight: bold;
}


/* --------------------------------------------------
   Tree Widget
-------------------------------------------------- */

QTreeWidget {
    background-color: #ffffff;
    color: #202020;

    border: 1px solid #d0d0d0;
}


/* --------------------------------------------------
   List Widget
-------------------------------------------------- */

QListWidget {
    background-color: #ffffff;
    color: #202020;

    border: 1px solid #d0d0d0;
}


/* --------------------------------------------------
   Tab Widget
-------------------------------------------------- */

QTabWidget::pane {
    border: 1px solid #d0d0d0;
    background-color: #ffffff;
}

QTabBar::tab {
    background-color: #ececec;
    color: #202020;

    padding: 8px 16px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
}


/* --------------------------------------------------
   Menu Bar
-------------------------------------------------- */

QMenuBar {
    background-color: #ffffff;
    color: #202020;
}

QMenuBar::item:selected {
    background-color: #e8e8e8;
}


/* --------------------------------------------------
   Menus
-------------------------------------------------- */

QMenu {
    background-color: #ffffff;
    color: #202020;
}

QMenu::item:selected {
    background-color: #e8e8e8;
}


/* --------------------------------------------------
   Status Bar
-------------------------------------------------- */

QStatusBar {
    background-color: #ececec;
    color: #202020;
}


/* --------------------------------------------------
   Scroll Bars
-------------------------------------------------- */

QScrollBar:vertical {
    background: #ececec;
    width: 12px;
}

QScrollBar::handle:vertical {
    background: #b0b0b0;
    min-height: 20px;
}

QScrollBar:horizontal {
    background: #ececec;
    height: 12px;
}

QScrollBar::handle:horizontal {
    background: #b0b0b0;
    min-width: 20px;
}

/* --------------------------------------------------
   Grid Table
-------------------------------------------------- */

QTableWidget {
    background-color: #FFFFFF;
    alternate-background-color: #F3F3F3;
    gridline-color: #D9D9D9;
}

QTableWidget::item:selected {
    background-color: #D6EAF8;
    color: #000000;
}

QTableWidget::item:selected:active {
    background-color: #AED6F1;
    color: #000000;
}

QTableWidget::item:hover {
    background-color: #AED6F1;
    color: #000000;
}
"""