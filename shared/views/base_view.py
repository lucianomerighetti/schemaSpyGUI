# Artefato:  base_view.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QMessageBox
)
from PyQt6.QtCore import Qt

class BaseView(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self._main_layout = QVBoxLayout()
        self._title = QLabel(title)
        self._title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        """)

        self._main_layout.addWidget(
            self._title
        )

        self.setLayout(
            self._main_layout
        )

    @property
    def content_layout(self):
        return self._main_layout

    def adjust_button_sizes(self, buttons: list[QPushButton]) -> None:
        """Ajusta o tamanho de todos os botões na lista para coincidir com o tamanho do maior texto."""
        if not buttons:
            return
        max_width = max(btn.fontMetrics().horizontalAdvance(btn.text()) + 40 for btn in buttons)
        for btn in buttons:
            btn.setFixedWidth(max_width)

    def configure_table(self, table: QTableWidget, columns: list[str]) -> None:
        """Configura e padroniza as opções visuais e de interação do QTableWidget fornecido."""
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSortingEnabled(True)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        table.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setStretchLastSection(True)
        header.setMinimumSectionSize(60)

    def auto_fit_columns(self, table: QTableWidget, margin: int = 20) -> None:
        """Redimensiona as colunas de uma tabela para ajustar ao conteúdo e adiciona uma margem."""
        table.resizeColumnsToContents()
        for col in range(table.columnCount()):
            w = table.columnWidth(col)
            table.setColumnWidth(col, w + margin)

    def show_message(self, title: str, message: str) -> None:
        """Exibe uma mensagem informativa."""
        QMessageBox.information(self, title, message)

    def show_warning_message(self, title: str, message: str) -> None:
        """Exibe uma mensagem de aviso/alerta."""
        QMessageBox.warning(self, title, message)

    def show_error_message(self, title: str, message: str) -> None:
        """Exibe uma mensagem crítica/erro."""
        QMessageBox.critical(self, title, message)

    def show_question_message(self, title: str, message: str) -> bool:
        """Exibe uma caixa de confirmação (Sim/Não) e retorna True se a resposta for Sim."""
        return QMessageBox.question(self, title, message) == QMessageBox.StandardButton.Yes

    def show_validation(self, report) -> None:
        """Exibe mensagens de validação com base em uma lista de relatórios de validação."""
        for r in report:
            if r.message:
                QMessageBox.warning(self, "Validação", r.message)