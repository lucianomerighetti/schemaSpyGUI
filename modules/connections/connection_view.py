# connection_view.py

from PyQt6.QtWidgets import (
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QFormLayout,
    QHBoxLayout,
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

class ConnectionView(BaseView):

    connection_selected = pyqtSignal(int)

    def __init__(self):
        super().__init__("Conexões")
        self._build_ui()

    def _build_ui(self):
        self.databases = (ConfigService.load_databases())
                
        # Formulário
        form_layout = QFormLayout()
        self.txt_conexao = QLineEdit()
        self.cbo_banco = QComboBox()
        self.cbo_banco.addItems([db["name"]for db in self.databases])
        self.txt_host = QLineEdit()
        self.txt_porta = QLineEdit()
        self.txt_porta.setValidator(QIntValidator(1, 65535))
        self.txt_database = QLineEdit()
        self.txt_schema = QLineEdit()
        self.txt_usuario = QLineEdit()
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_caminho = QLineEdit()
        self.txt_jdbc_driver = QLineEdit()
        self.txt_jdbc_url = QLineEdit()
        self.chk_ativo = QCheckBox()
        
        self.cbo_banco.currentTextChanged.connect(self._on_database_changed)
        self._on_database_changed(self.cbo_banco.currentText())
        
        form_layout.addRow(QLabel("Nome Conexão"), self.txt_conexao)
        form_layout.addRow(QLabel("Banco"), self.cbo_banco)
        form_layout.addRow(QLabel("Host"), self.txt_host)
        form_layout.addRow(QLabel("Porta"), self.txt_porta)
        form_layout.addRow(QLabel("Database"), self.txt_database)
        form_layout.addRow(QLabel("Schema"), self.txt_schema)
        form_layout.addRow(QLabel("Usuário"), self.txt_usuario)
        form_layout.addRow(QLabel("Senha"), self.txt_password)
        form_layout.addRow(QLabel("Caminho"), self.txt_caminho)
        form_layout.addRow(QLabel("JDBC Driver"), self.txt_jdbc_driver)
        form_layout.addRow(QLabel("JDBC URL"), self.txt_jdbc_url)
        form_layout.addRow(QLabel("Ativo"), self.chk_ativo)

        button_layout = QHBoxLayout()
        self.btn_new = QPushButton("Novo")
        self.btn_save = QPushButton("Salvar")
        self.btn_delete = QPushButton("Excluir")
        self.btn_test = QPushButton("Testar Conexão")
        
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_delete)
        button_layout.addWidget(self.btn_test)
        button_layout.addStretch()

        self.tbl_connections = (QTableWidget())
        self.current_connection_id = None
        self.tbl_connections.setColumnCount(9)
        self.tbl_connections.setHorizontalHeaderLabels(["ID", "Nome", "Banco", "Host", "Porta", "Database", "Schema", "Usuário", "Ativo"])

        header = (self.tbl_connections.horizontalHeader())
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, 7):
            header.setSectionResizeMode(col,QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)
        #header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        #header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        #header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        #header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        #header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        #header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        #header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)
        #header.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)
        #header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)            
        #header.setStretchLastSection(False)
        
        self.tbl_connections.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tbl_connections.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.tbl_connections.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tbl_connections.itemSelectionChanged.connect(self._on_selection_changed)

        for col in range(self.tbl_connections.columnCount()):
            if col in (0, 3, 8):
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
            else:
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)

        self.tbl_connections.setAlternatingRowColors(True)
        self.tbl_connections.setSortingEnabled(True)
        self.tbl_connections.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tbl_connections.setVerticalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)        
        
        # Montagem da tela
        self.content_layout.addLayout(form_layout)
        self.content_layout.addLayout(button_layout)
        self.content_layout.addWidget(self.tbl_connections)

    def clear_form(self):
        self.current_connection_id = None
        self.txt_conexao.clear()
        self.cbo_banco.setCurrentIndex(0)
        self.txt_host.clear()
        self.txt_porta.clear()
        self.txt_database.clear()
        self.txt_schema.clear()
        self.txt_usuario.clear()
        self.txt_password.clear()
        self.txt_caminho.clear()
        self.txt_jdbc_driver.clear()
        self.txt_jdbc_url.clear()
        #self.chk_ativo.setChecked(False)
        self.chk_ativo.setChecked(True)

    def populate_grid(self, connections):
        self.tbl_connections.setRowCount(0)
        for row, connection in enumerate(connections):
            self.tbl_connections.insertRow(row)
            self.tbl_connections.setItem(row, 0, QTableWidgetItem(str(connection.id_conexao)))
            self.tbl_connections.setItem(row, 1, QTableWidgetItem(connection.nm_conexao))
            self.tbl_connections.setItem(row, 2, QTableWidgetItem(connection.tp_database))
            self.tbl_connections.setItem(row, 3, QTableWidgetItem(connection.nm_host))
            self.tbl_connections.setItem(row, 4, QTableWidgetItem(str(connection.nu_porta)))
            self.tbl_connections.setItem(row, 5, QTableWidgetItem(connection.nm_database))
            self.tbl_connections.setItem(row, 6, QTableWidgetItem(connection.nm_schema))
            self.tbl_connections.setItem(row, 7, QTableWidgetItem(connection.nm_usuario))
            self.tbl_connections.setItem(row, 8, QTableWidgetItem("Sim" if connection.fl_ativo else "Não"))

    def get_selected_id_conexao(self):
        row = (self.tbl_connections.currentRow())

        if row < 0:
            return None

        item = (self.tbl_connections.item(row, 0))

        if item is None:
            return None

        return int(item.text())

    def load_connection(self, connection):
        self.current_connection_id = (connection.id_conexao)
        self.txt_conexao.setText(connection.nm_conexao)
        self.cbo_banco.setCurrentText(connection.tp_database)
        self.txt_host.setText(connection.nm_host)
        self.txt_porta.setText(str(connection.nu_porta))
        self.txt_database.setText(connection.nm_database)
        self.txt_schema.setText(connection.nm_schema)
        self.txt_usuario.setText(connection.nm_usuario)
        self.txt_password.setText(connection.tx_password)
        self.txt_caminho.setText(connection.ds_caminho)
        self.txt_jdbc_driver.setText(connection.ds_jdbc_driver)
        self.txt_jdbc_url.setText(connection.ds_jdbc_url)
        self.chk_ativo.setChecked(connection.fl_ativo)

    def _on_selection_changed(self):
        row = (self.tbl_connections.currentRow())

        if row < 0:
            return

        id_conexao = int(self.tbl_connections.item(row, 0).text())
        self.connection_selected.emit(id_conexao)

    def _on_database_changed(self, database_name):
        database = next((db for db in self.databases if db["name"] == database_name), None)

        if not database:
            return

        default_port = (database.get("default_port", 0))
        default_driver = (database.get("driver", 0))
        default_url = (database.get("jdbc_template", 0))

        self.txt_porta.setText(str(default_port))
        self.txt_jdbc_driver.setText(str(default_driver))
        self.txt_jdbc_url.setText(str(default_url))