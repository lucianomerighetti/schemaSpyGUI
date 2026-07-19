# modules/projects/import_dialog.py
from PyQt6.QtWidgets import (
    QDialog,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QFormLayout,
    QMessageBox,
    QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from shared.services.config_service import ConfigService

# BUG FIX: Implementação - Diálogo de Edição de Linha de Importação
class EditImportRowDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Projeto para Importação")
        self.resize(400, 300)
        self.data = data
        self.databases = ConfigService.load_databases()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.txt_nome = QLineEdit(self.data.get("nm_projeto", ""))
        self.cbo_banco = QComboBox()
        self.cbo_banco.addItems([db["name"] for db in self.databases])
        self.cbo_banco.setCurrentText(self.data.get("tp_database", ""))
        
        self.txt_database = QLineEdit(self.data.get("nm_database", ""))
        self.txt_host = QLineEdit(self.data.get("nm_host", ""))
        self.txt_schema = QLineEdit(self.data.get("nm_schema", ""))
        
        porta_val = self.data.get("nu_porta")
        self.txt_porta = QLineEdit(str(porta_val) if porta_val is not None else "")
        self.txt_porta.setValidator(QIntValidator(1, 65535))

        form_layout.addRow(QLabel("Nome Projeto"), self.txt_nome)
        form_layout.addRow(QLabel("Banco"), self.cbo_banco)
        form_layout.addRow(QLabel("Database"), self.txt_database)
        form_layout.addRow(QLabel("Host"), self.txt_host)
        form_layout.addRow(QLabel("Schema"), self.txt_schema)
        form_layout.addRow(QLabel("Porta"), self.txt_porta)

        # Botões
        button_layout = QHBoxLayout()
        self.btn_save = QPushButton("Salvar")
        self.btn_cancel = QPushButton("Cancelar")
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_cancel)
        button_layout.addStretch()

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.btn_save.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

    def get_data(self):
        porta_str = self.txt_porta.text().strip()
        try:
            porta = int(porta_str) if porta_str else None
        except ValueError:
            porta = None

        return {
            "nm_projeto": self.txt_nome.text().strip(),
            "tp_database": self.cbo_banco.currentText(),
            "nm_database": self.txt_database.text().strip(),
            "nm_host": self.txt_host.text().strip(),
            "nm_schema": self.txt_schema.text().strip(),
            "nu_porta": porta
        }


# BUG FIX: Implementação - Diálogo Principal de Importação de Projetos
class ImportProjectsDialog(QDialog):
    def __init__(self, projects_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Importar Projetos")
        self.resize(850, 500)
        self.projects_data = projects_data
        self._build_ui()
        self.load_data()

    def _build_ui(self):
        main_layout = QVBoxLayout()

        # Botões Superiores
        buttons_layout = QHBoxLayout()
        self.btn_edit = QPushButton("Editar")
        self.btn_delete = QPushButton("Excluir")
        self.btn_import = QPushButton("Importar")
        self.btn_cancel = QPushButton("Cancelar")

        buttons_layout.addWidget(self.btn_edit)
        buttons_layout.addWidget(self.btn_delete)
        buttons_layout.addWidget(self.btn_import)
        buttons_layout.addWidget(self.btn_cancel)
        buttons_layout.addStretch()

        # Grid de Importação (tbl_import)
        self.tbl_import = QTableWidget()
        columns = ["Importar", "Nome", "Banco", "Database", "Host", "Schema", "Porta"]
        self.tbl_import.setColumnCount(len(columns))
        self.tbl_import.setHorizontalHeaderLabels(columns)
        self.tbl_import.setAlternatingRowColors(True)
        self.tbl_import.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tbl_import.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tbl_import.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Configurar modo de redimensionamento proporcional
        header = self.tbl_import.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Checkbox
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents) # Porta

        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.tbl_import)
        self.setLayout(main_layout)

        # Conectar ações dos botões
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)
        self.btn_import.clicked.connect(self._on_import)
        self.btn_cancel.clicked.connect(self.reject)

    def load_data(self):
        self.tbl_import.setRowCount(0)
        for row, item in enumerate(self.projects_data):
            self.tbl_import.insertRow(row)

            # Checkbox de importação na primeira coluna
            chk_item = QTableWidgetItem()
            chk_item.setCheckState(Qt.CheckState.Checked)
            self.tbl_import.setItem(row, 0, chk_item)

            # Mapeia chaves de nomes em pt/en no dicionário
            nome = item.get("nm_projeto") or item.get("nome") or item.get("nmProjeto") or ""
            banco = item.get("tp_database") or item.get("banco") or item.get("tipoBanco") or ""
            database = item.get("nm_database") or item.get("database") or item.get("nomeBanco") or ""
            host = item.get("nm_host") or item.get("host") or ""
            schema = item.get("nm_schema") or item.get("schema") or ""
            porta = item.get("nu_porta") or item.get("porta") or ""

            self.tbl_import.setItem(row, 1, QTableWidgetItem(nome))
            self.tbl_import.setItem(row, 2, QTableWidgetItem(banco))
            self.tbl_import.setItem(row, 3, QTableWidgetItem(database))
            self.tbl_import.setItem(row, 4, QTableWidgetItem(host))
            self.tbl_import.setItem(row, 5, QTableWidgetItem(schema))
            self.tbl_import.setItem(row, 6, QTableWidgetItem(str(porta)))

    def _get_row_data(self, row):
        try:
            porta_str = self.tbl_import.item(row, 6).text().strip()
            porta = int(porta_str) if porta_str else None
        except ValueError:
            porta = None

        return {
            "nm_projeto": self.tbl_import.item(row, 1).text(),
            "tp_database": self.tbl_import.item(row, 2).text(),
            "nm_database": self.tbl_import.item(row, 3).text(),
            "nm_host": self.tbl_import.item(row, 4).text(),
            "nm_schema": self.tbl_import.item(row, 5).text(),
            "nu_porta": porta
        }

    def _on_edit(self):
        selected_row = self.tbl_import.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma linha para editar.")
            return

        current_data = self._get_row_data(selected_row)
        dialog = EditImportRowDialog(current_data, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            self.tbl_import.setItem(selected_row, 1, QTableWidgetItem(new_data["nm_projeto"]))
            self.tbl_import.setItem(selected_row, 2, QTableWidgetItem(new_data["tp_database"]))
            self.tbl_import.setItem(selected_row, 3, QTableWidgetItem(new_data["nm_database"]))
            self.tbl_import.setItem(selected_row, 4, QTableWidgetItem(new_data["nm_host"]))
            self.tbl_import.setItem(selected_row, 5, QTableWidgetItem(new_data["nm_schema"]))
            self.tbl_import.setItem(selected_row, 6, QTableWidgetItem(str(new_data["nu_porta"]) if new_data["nu_porta"] is not None else ""))

    def _on_delete(self):
        selected_row = self.tbl_import.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma linha para excluir.")
            return

        if QMessageBox.question(self, "Confirmação", "Deseja remover este item da lista de importação?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.tbl_import.removeRow(selected_row)

    def _on_import(self):
        # Filtra os dados apenas das linhas cujos checkboxes estão marcados
        self.selected_projects = []
        for row in range(self.tbl_import.rowCount()):
            chk_item = self.tbl_import.item(row, 0)
            if chk_item and chk_item.checkState() == Qt.CheckState.Checked:
                self.selected_projects.append(self._get_row_data(row))

        if not self.selected_projects:
            QMessageBox.warning(self, "Aviso", "Nenhum projeto marcado para importação.")
            return

        self.accept()

    def get_imported_projects(self):
        return self.selected_projects
