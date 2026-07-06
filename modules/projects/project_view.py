# project_view.py

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QHeaderView
)
from PyQt6.QtCore import (
    Qt
)
from PyQt6.QtGui import (
    QIntValidator
)
from PyQt6.QtCore import (
    pyqtSignal
)
from shared.views.base_view import (
    BaseView
)
from shared.services.config_service import (
    ConfigService
)

class ProjectView(BaseView):

    project_selected = pyqtSignal(int)

    def __init__(self):
        super().__init__("Projetos")
        self._build_ui()

    def _build_ui(self):
        self.databases = (ConfigService.load_databases())
                
        # Formulário
        form_layout = QFormLayout()
        self.txt_projeto = QLineEdit()
        self.cbo_banco = QComboBox()
        self.cbo_banco.addItems([db["name"]for db in self.databases])
        self.txt_host = QLineEdit()
        self.txt_schema = QLineEdit()
        self.txt_porta = QLineEdit()
        self.txt_porta.setValidator(QIntValidator(1, 65535))
        
        self.cbo_banco.currentTextChanged.connect(self._on_database_changed)        
        self._on_database_changed(self.cbo_banco.currentText())

        form_layout.addRow(QLabel("Nome Projeto"), self.txt_projeto)
        form_layout.addRow(QLabel("Banco"), self.cbo_banco)
        form_layout.addRow(QLabel("Host"), self.txt_host)
        form_layout.addRow(QLabel("Schema"), self.txt_schema)
        form_layout.addRow(QLabel("Porta"), self.txt_porta)

        # Botões
        button_layout = QHBoxLayout()

        self.btn_new = QPushButton("Novo")
        self.btn_save = QPushButton("Salvar")
        self.btn_delete = QPushButton("Excluir")

        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_delete)
        button_layout.addStretch()

        # Grid
        self.tbl_projects = QTableWidget()
        self.tbl_projects.setAlternatingRowColors(True)
        self.tbl_projects.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.current_project_id = None
        self.tbl_projects.setColumnCount(6)
        self.tbl_projects.setHorizontalHeaderLabels(["ID", "Nome", "Banco", "Host", "Schema", "Porta"])
        
        header = self.tbl_projects.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        
        self.tbl_projects.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tbl_projects.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tbl_projects.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tbl_projects.itemSelectionChanged.connect(self._on_selection_changed)
        
        # Montagem da tela
        self.content_layout.addLayout(form_layout)
        self.content_layout.addLayout(button_layout)
        self.content_layout.addWidget(self.tbl_projects)

    def clear_form(self):
        self.current_project_id = None
        self.txt_projeto.clear()
        self.cbo_banco.setCurrentIndex(0)
        self.txt_host.clear()
        self.txt_schema.clear()
        self.txt_porta.clear()

    def populate_grid(self, projects):
        self.tbl_projects.setRowCount(0)
        for row, project in enumerate(projects):
            self.tbl_projects.insertRow(row)
            self.tbl_projects.setItem(row, 0, QTableWidgetItem(str(project.id_projeto)))
            self.tbl_projects.setItem(row, 1, QTableWidgetItem(project.nm_projeto))
            self.tbl_projects.setItem(row, 2, QTableWidgetItem(project.tp_database))
            self.tbl_projects.setItem(row, 3, QTableWidgetItem(project.nm_host))
            self.tbl_projects.setItem(row, 4, QTableWidgetItem(project.nm_schema))
            self.tbl_projects.setItem(row, 5, QTableWidgetItem(str(project.nu_porta)))

    def get_selected_id_projeto(self):
        row = self.tbl_projects.currentRow()
        if row < 0:
            return None

        item = self.tbl_projects.item(row, 0)

        if item is None:
            return None

        return int(item.text())
    
    def load_project(self, project):
        self.current_project_id = project.id_projeto
        self.txt_projeto.setText(project.nm_projeto)
        self.cbo_banco.setCurrentText(project.tp_database)
        self.txt_host.setText(project.nm_host)
        self.txt_schema.setText(project.nm_schema)
        self.txt_porta.setText(str(project.nu_porta))
        
    def _on_selection_changed(self):
        row = self.tbl_projects.currentRow()
        if row < 0:
            return

        id_projeto = int(self.tbl_projects.item(row,0).text())

        self.project_selected.emit(id_projeto)

    def _on_database_changed(self, database_name):
        database = next((db for db in self.databases if db["name"] == database_name), None)

        if not database:
            return

        default_port = (database.get("default_port", 0))
        
        self.txt_porta.setText(str(default_port))
