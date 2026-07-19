# Artefato:  project_view.py

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
from .project_dto import ProjectDTO

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
        self.txt_database = QLineEdit()
        self.txt_schema = QLineEdit()
        self.txt_porta = QLineEdit()
        self.txt_porta.setValidator(QIntValidator(1, 65535))
        
        self.cbo_banco.currentTextChanged.connect(self._on_database_changed)        
        self._on_database_changed(self.cbo_banco.currentText())

        # BUG FIX: Alteração - Formulário de projeto agora comporta o campo Database
        form_layout.addRow(QLabel("Nome Projeto"), self.txt_projeto)
        form_layout.addRow(QLabel("Banco"), self.cbo_banco)
        form_layout.addRow(QLabel("Host"), self.txt_host)
        form_layout.addRow(QLabel("Database"), self.txt_database)
        form_layout.addRow(QLabel("Schema"), self.txt_schema)
        form_layout.addRow(QLabel("Porta"), self.txt_porta)

        # Botões
        button_layout = QHBoxLayout()

        self.btn_new = QPushButton("Novo")
        self.btn_save = QPushButton("Salvar")
        self.btn_delete = QPushButton("Excluir")
        self.btn_import = QPushButton("Importar")

        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_delete)
        button_layout.addWidget(self.btn_import)
        button_layout.addStretch()

        # BUG FIX: Alteração - Todos os botões devem possuir o mesmo tamanho (utilizando a classe base BaseView)
        self.adjust_button_sizes([self.btn_new, self.btn_save, self.btn_delete, self.btn_import])

        # Grid
        self.tbl_projects = QTableWidget()
        self.current_project_id = None
        # BUG FIX: Alteração - Coluna Database inserida na Grid de projetos
        self.configure_table(self.tbl_projects, ["ID", "Nome", "Banco", "Host", "Database", "Schema", "Porta"])
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
        self.txt_database.clear()
        self.txt_schema.clear()
        self.txt_porta.clear()

    def populate_grid(self, projects):
        # BUG FIX: Alteração - Desabilitar temporariamente a ordenação ao popular a grid para evitar desalinhamento de linhas
        self.tbl_projects.setSortingEnabled(False)
        self.tbl_projects.setRowCount(0)
        for row, project in enumerate(projects):
            self.tbl_projects.insertRow(row)
            self.tbl_projects.setItem(row, 0, QTableWidgetItem(str(project.id_projeto)))
            self.tbl_projects.setItem(row, 1, QTableWidgetItem(project.nm_projeto))
            self.tbl_projects.setItem(row, 2, QTableWidgetItem(project.tp_database))
            self.tbl_projects.setItem(row, 3, QTableWidgetItem(project.nm_host or ""))
            self.tbl_projects.setItem(row, 4, QTableWidgetItem(project.nm_database or ""))
            self.tbl_projects.setItem(row, 5, QTableWidgetItem(project.nm_schema or ""))
            self.tbl_projects.setItem(row, 6, QTableWidgetItem(str(project.nu_porta) if project.nu_porta is not None else ""))
        
        # BUG FIX: Alteração - Usando utilitário auto_fit_columns herdado de BaseView
        self.auto_fit_columns(self.tbl_projects)
        
        # BUG FIX: Alteração - Coluna Porta (índice 6) com tamanho fixo correspondente ao tamanho do texto
        self.tbl_projects.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        self.tbl_projects.setSortingEnabled(True)

    def get_selected_id_projeto(self):
        row = self.tbl_projects.currentRow()
        if row < 0:
            return None

        item = self.tbl_projects.item(row, 0)

        if item is None:
            return None

        return int(item.text())

    def get_project(self) -> ProjectDTO:
        try:
            porta_str = self.txt_porta.text().strip()
            porta = int(porta_str) if porta_str else None
        except ValueError:
            porta = None

        return ProjectDTO(
            id_projeto=self.current_project_id,
            nm_projeto=self.txt_projeto.text(),
            tp_database=self.cbo_banco.currentText(),
            nm_database=self.txt_database.text(),
            nm_host=self.txt_host.text(),
            nm_schema=self.txt_schema.text(),
            nu_porta=porta
        )
    
    def load_project(self, project):
        self.current_project_id = project.id_projeto
        self.txt_projeto.setText(project.nm_projeto or "")
        self.cbo_banco.setCurrentText(project.tp_database or "")
        self.txt_host.setText(project.nm_host or "")
        self.txt_database.setText(project.nm_database or "")
        self.txt_schema.setText(project.nm_schema or "")
        self.txt_porta.setText(str(project.nu_porta) if project.nu_porta is not None else "")
        
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

        default_port = database.get("default_port", 0)
        
        self.txt_porta.setText(str(default_port))

        # Toggling dinâmico de campos baseados em arquivo vs servidor
        is_file_db = database_name.lower() in ("sqlite", "access", "firebird_embedded", "duckdb")
        self.txt_host.setEnabled(not is_file_db)
        self.txt_database.setEnabled(not is_file_db)
        self.txt_schema.setEnabled(not is_file_db)
        self.txt_porta.setEnabled(not is_file_db)
