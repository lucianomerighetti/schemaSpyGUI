# dark_theme.py

DARK_THEME = """
QMainWindow {
    background-color: #18181b; /* Fundo: grafite profundo */
}

QWidget {
    color: #ffffff; /* Tipografia: Branco puro para textos principais */
    background-color: #18181b; /* Fundo: grafite profundo */
    font-family: Segoe UI;
    font-size: 10pt;
}

QFrame {
    background-color: #242427;
}

/* Tipografia: Cinza claro para textos secundários */
QLabel {
    color: #a1a1aa; /* Cinza claro */
}

/* Textos principais brancos para botões, inputs, etc. */
QPushButton, QLineEdit, QComboBox, QCheckBox, QTableWidget {
    color: #ffffff;
}

QLineEdit, QComboBox {
    background-color: #242427;
    border: 1px solid #d4d4d8; /* Divisórias/bordas: cinza claro */
    border-radius: 4px;
    padding: 6px;
}

QComboBox::drop-down {
    border: none;
}

QPushButton {
    background-color: #2e2e33;
    border: 1px solid #52525b;
    border-radius: 4px;
    padding: 8px 12px;
    text-align: left;
}

QPushButton:hover {
    background-color: #3f3f46;
}

QStatusBar {
    background-color: #242427;
    color: #a1a1aa; /* Cinza claro para texto do status bar */
}

/* --------------------------------------------------
   Grid Table
-------------------------------------------------- */

QTableWidget {
    background-color: #18181b;
    alternate-background-color: #242427; /* Linhas zebradas */
    gridline-color: #d4d4d8; /* Divisórias da grid: Linhas finas em cinza claro */
    border: 1px solid #d4d4d8;
}

QHeaderView::section {
    background-color: #242427;
    color: #ffffff;
    padding: 5px;
    border: 1px solid #d4d4d8; /* Linhas finas em cinza claro para os divisores do header */
}

QTableWidget::item:selected {
    background-color: #3f3f46;
    color: #ffffff;
}

QTableWidget::item:hover {
    background-color: #2e2e33;
}
"""