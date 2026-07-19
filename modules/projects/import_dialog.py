# modules/projects/import_dialog.py
import os
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

# BUG FIX: Implementação - Função utilitária para ler o arquivo .env de importação de data/.env
def load_import_env():
    """
    Lê o arquivo .env na pasta data do projeto, mapeando chaves em vetores de strings.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # schemaSpyGUI/modules/projects/import_dialog.py -> subir dois níveis
    project_root = os.path.dirname(os.path.dirname(current_dir))
    env_path = os.path.join(project_root, "data", ".env")
    
    env = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    env[key.strip()] = [v.strip() for v in val.split(",")]
    return env

# BUG FIX: Implementação - Função auxiliar de aplanamento dinâmico de dicionário
def flatten_item(item):
    flat = {}
    for k, v in item.items():
        if isinstance(v, dict):
            for ik, iv in v.items():
                if ik not in flat:
                    flat[ik] = iv
            for ik, iv in v.items():
                flat[f"{k}_{ik}"] = iv
        else:
            flat[k] = v
    return flat

# BUG FIX: Implementação - Mapeamento heurístico unificado parametrizado por .env
def map_item_to_project(item, databases, env=None):
    if not env:
        env = {}
        
    proj_nm_projeto_keys = env.get("PROJ_NM_PROJETO", ["ConnName", "name"])
    proj_tp_database_keys = env.get("PROJ_TP_DATABASE", ["RaptorConnectionType", "provider", "driver", "type"])
    proj_nm_host_keys = env.get("PROJ_NM_HOST", ["hostname", "host", "configuration.host"])
    proj_nm_schema_keys = env.get("PROJ_NM_SCHEMA", ["serviceName", "configuration.database"])
    proj_nu_porta_keys = env.get("PROJ_NU_PORTA", ["port", "configuration.port"])
    proj_nm_database_keys = env.get("PROJ_NM_DATABASE", ["serviceName", "info_sid", "configuration.database"])

    conn_nm_usuario_keys = env.get("CONN_NM_USUARIO", ["user", "configuration.user", "configuration.userName"])
    conn_tx_password_keys = env.get("CONN_TX_PASSWORD", ["user", "password", "configuration.password"])
    conn_ds_caminho_keys = env.get("CONN_DS_CAMINHO", ["database", "configuration.database"])
    conn_ds_jdbc_driver_keys = env.get("CONN_DS_JDBC_DRIVER", ["driver", "provider"])
    conn_ds_jdbc_url_keys = env.get("CONN_DS_JDBC_URL", ["customUrl", "url", "configuration.url"])

    def get_value(keys):
        for key in keys:
            # 1. Tenta buscar a chave exata no item aplanado
            if key in item:
                return item[key]
            # 2. Tenta buscar substituindo ponto por underscore
            flat_key = key.replace(".", "_")
            if flat_key in item:
                return item[flat_key]
            # 3. Tenta buscar apenas a última parte se contiver ponto (ex: 'host' em 'configuration.host')
            if "." in key:
                last_part = key.split(".")[-1]
                if last_part in item:
                    return item[last_part]
        return ""

    # 1. Nome do Projeto
    nm_projeto = str(get_value(proj_nm_projeto_keys)).strip()

    # 2. Banco (Tipo de Banco)
    tp_database = "SQLite"
    raw_banco = str(get_value(proj_tp_database_keys)).lower()
    
    if raw_banco:
        if "oracle" in raw_banco:
            tp_database = "Oracle"
        elif "sqlserver" in raw_banco or "sql server" in raw_banco or "microsoft" in raw_banco:
            tp_database = "SQL Server"
        elif "mysql" in raw_banco:
            tp_database = "MySQL"
        elif "postgres" in raw_banco or "postgresql" in raw_banco:
            tp_database = "PostgreSQL"
        elif "firebird" in raw_banco:
            tp_database = "Firebird"
        elif "mariadb" in raw_banco:
            tp_database = "MariaDB"
        elif "sqlite" in raw_banco:
            tp_database = "SQLite"
        elif "access" in raw_banco:
            tp_database = "Access"
        else:
            for db in databases:
                if db["name"].lower() == raw_banco:
                    tp_database = db["name"]
                    break

    # 3. Database
    nm_database = str(get_value(proj_nm_database_keys)).strip()

    # 4. Host
    nm_host = str(get_value(proj_nm_host_keys)).strip()

    # 5. Schema
    nm_schema = str(get_value(proj_nm_schema_keys)).strip()

    # 6. Porta
    nu_porta = None
    porta_val = get_value(proj_nu_porta_keys)
    if porta_val:
        try:
            nu_porta = int(str(porta_val).strip())
        except ValueError:
            pass

    # 7. Usuário
    nm_usuario = str(get_value(conn_nm_usuario_keys)).strip()

    # 8. Senha
    tx_password = str(get_value(conn_tx_password_keys)).strip()

    # 9. Caminho
    ds_caminho = str(get_value(conn_ds_caminho_keys)).strip()

    # 10. Driver JDBC
    ds_jdbc_driver = str(get_value(conn_ds_jdbc_driver_keys)).strip()

    # 11. URL JDBC
    ds_jdbc_url = str(get_value(conn_ds_jdbc_url_keys)).strip()

    return {
        "nm_projeto": nm_projeto,
        "tp_database": tp_database,
        "nm_database": nm_database,
        "nm_host": nm_host,
        "nm_schema": nm_schema,
        "nu_porta": nu_porta,
        "nm_usuario": nm_usuario,
        "tx_password": tx_password,
        "ds_caminho": ds_caminho,
        "ds_jdbc_driver": ds_jdbc_driver,
        "ds_jdbc_url": ds_jdbc_url
    }


# BUG FIX: Implementação - Diálogo de Edição de Linha de Importação Completa (11 campos)
class EditImportRowDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Projeto e Conexão para Importação")
        self.resize(500, 480)
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
        
        self.txt_host = QLineEdit(self.data.get("nm_host", ""))
        porta_val = self.data.get("nu_porta")
        self.txt_porta = QLineEdit(str(porta_val) if porta_val is not None else "")
        self.txt_porta.setValidator(QIntValidator(1, 65535))

        self.txt_database = QLineEdit(self.data.get("nm_database", ""))
        self.txt_schema = QLineEdit(self.data.get("nm_schema", ""))
        self.txt_usuario = QLineEdit(self.data.get("nm_usuario", ""))
        self.txt_senha = QLineEdit(self.data.get("tx_password", ""))
        self.txt_caminho = QLineEdit(self.data.get("ds_caminho", ""))
        self.txt_driver = QLineEdit(self.data.get("ds_jdbc_driver", ""))
        self.txt_url = QLineEdit(self.data.get("ds_jdbc_url", ""))

        form_layout.addRow(QLabel("Nome Conexão/Projeto"), self.txt_nome)
        form_layout.addRow(QLabel("Banco"), self.cbo_banco)
        form_layout.addRow(QLabel("Host"), self.txt_host)
        form_layout.addRow(QLabel("Porta"), self.txt_porta)
        form_layout.addRow(QLabel("Database"), self.txt_database)
        form_layout.addRow(QLabel("Schema"), self.txt_schema)
        form_layout.addRow(QLabel("Usuário"), self.txt_usuario)
        form_layout.addRow(QLabel("Senha"), self.txt_senha)
        form_layout.addRow(QLabel("Caminho (SQLite)"), self.txt_caminho)
        form_layout.addRow(QLabel("Driver JDBC"), self.txt_driver)
        form_layout.addRow(QLabel("URL JDBC"), self.txt_url)

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
            "nu_porta": porta,
            "nm_usuario": self.txt_usuario.text().strip(),
            "tx_password": self.txt_senha.text().strip(),
            "ds_caminho": self.txt_caminho.text().strip(),
            "ds_jdbc_driver": self.txt_driver.text().strip(),
            "ds_jdbc_url": self.txt_url.text().strip()
        }


# BUG FIX: Implementação - Diálogo Principal de Importação Exibindo Apenas Campos do .env
class ImportProjectsDialog(QDialog):
    def __init__(self, raw_projects_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Importar Projetos e Conexões")
        self.resize(1100, 600)
        self.databases = ConfigService.load_databases()
        
        # Carregar .env de importação
        self.import_env = load_import_env()
        
        # Aplanar os dados recebidos do JSON
        self.flat_items = [flatten_item(item) for item in raw_projects_data]
        
        # Lista correspondente de projetos e conexões mapeados
        self.mapped_projects = [map_item_to_project(item, self.databases, self.import_env) for item in self.flat_items]
        
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

        # Grid de Importação Mapeada (tbl_import com colunas correspondentes às tabelas)
        self.tbl_import = QTableWidget()
        columns = [
            "Importar", "Nome", "Banco", "Host", "Porta", 
            "Database", "Schema", "Usuário", "Senha", 
            "Caminho", "Driver JDBC", "URL JDBC"
        ]
        self.tbl_import.setColumnCount(len(columns))
        self.tbl_import.setHorizontalHeaderLabels(columns)
        self.tbl_import.setAlternatingRowColors(True)
        self.tbl_import.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tbl_import.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tbl_import.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Configurar redimensionamento interativo e fixar checkbox
        header = self.tbl_import.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Checkbox

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
        for row, mapped_data in enumerate(self.mapped_projects):
            self.tbl_import.insertRow(row)

            # Checkbox de importação na primeira coluna
            chk_item = QTableWidgetItem()
            chk_item.setCheckState(Qt.CheckState.Checked)
            self.tbl_import.setItem(row, 0, chk_item)

            # Preencher as colunas com base nos dados mapeados
            self.tbl_import.setItem(row, 1, QTableWidgetItem(mapped_data["nm_projeto"]))
            self.tbl_import.setItem(row, 2, QTableWidgetItem(mapped_data["tp_database"]))
            self.tbl_import.setItem(row, 3, QTableWidgetItem(mapped_data["nm_host"]))
            porta_str = str(mapped_data["nu_porta"]) if mapped_data["nu_porta"] is not None else ""
            self.tbl_import.setItem(row, 4, QTableWidgetItem(porta_str))
            self.tbl_import.setItem(row, 5, QTableWidgetItem(mapped_data["nm_database"]))
            self.tbl_import.setItem(row, 6, QTableWidgetItem(mapped_data["nm_schema"]))
            self.tbl_import.setItem(row, 7, QTableWidgetItem(mapped_data["nm_usuario"]))
            self.tbl_import.setItem(row, 8, QTableWidgetItem(mapped_data["tx_password"]))
            self.tbl_import.setItem(row, 9, QTableWidgetItem(mapped_data["ds_caminho"]))
            self.tbl_import.setItem(row, 10, QTableWidgetItem(mapped_data["ds_jdbc_driver"]))
            self.tbl_import.setItem(row, 11, QTableWidgetItem(mapped_data["ds_jdbc_url"]))
                
        # Redimensiona para os conteúdos de cada coluna
        self.tbl_import.resizeColumnsToContents()

    def _on_edit(self):
        selected_row = self.tbl_import.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma linha para editar.")
            return

        current_mapped_data = self.mapped_projects[selected_row]
        dialog = EditImportRowDialog(current_mapped_data, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_mapped_data = dialog.get_data()
            self.mapped_projects[selected_row] = new_mapped_data
            
            # Sincronização visual imediata de todos os 11 campos na grid
            self.tbl_import.setItem(selected_row, 1, QTableWidgetItem(new_mapped_data["nm_projeto"]))
            self.tbl_import.setItem(selected_row, 2, QTableWidgetItem(new_mapped_data["tp_database"]))
            self.tbl_import.setItem(selected_row, 3, QTableWidgetItem(new_mapped_data["nm_host"]))
            porta_str = str(new_mapped_data["nu_porta"]) if new_mapped_data["nu_porta"] is not None else ""
            self.tbl_import.setItem(selected_row, 4, QTableWidgetItem(porta_str))
            self.tbl_import.setItem(selected_row, 5, QTableWidgetItem(new_mapped_data["nm_database"]))
            self.tbl_import.setItem(selected_row, 6, QTableWidgetItem(new_mapped_data["nm_schema"]))
            self.tbl_import.setItem(selected_row, 7, QTableWidgetItem(new_mapped_data["nm_usuario"]))
            self.tbl_import.setItem(selected_row, 8, QTableWidgetItem(new_mapped_data["tx_password"]))
            self.tbl_import.setItem(selected_row, 9, QTableWidgetItem(new_mapped_data["ds_caminho"]))
            self.tbl_import.setItem(selected_row, 10, QTableWidgetItem(new_mapped_data["ds_jdbc_driver"]))
            self.tbl_import.setItem(selected_row, 11, QTableWidgetItem(new_mapped_data["ds_jdbc_url"]))

    def _on_delete(self):
        selected_row = self.tbl_import.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione uma linha para excluir.")
            return

        if QMessageBox.question(self, "Confirmação", "Deseja remover este item da lista de importação?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.tbl_import.removeRow(selected_row)
            self.mapped_projects.pop(selected_row)
            self.flat_items.pop(selected_row)

    def _on_import(self):
        self.selected_projects = []
        for row in range(self.tbl_import.rowCount()):
            chk_item = self.tbl_import.item(row, 0)
            if chk_item and chk_item.checkState() == Qt.CheckState.Checked:
                # Retorna tupla contendo o projeto mapeado e os dados aplanados brutos
                self.selected_projects.append((self.mapped_projects[row], self.flat_items[row]))

        if not self.selected_projects:
            QMessageBox.warning(self, "Aviso", "Nenhum projeto marcado para importação.")
            return

        self.accept()

    def get_imported_projects(self):
        return self.selected_projects
