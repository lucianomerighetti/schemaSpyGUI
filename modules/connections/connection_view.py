# Artefato:  connection_view.py
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
from .connection_dto import ConnectionDTO

class ConnectionView(BaseView):

    connection_selected = pyqtSignal(int)

    def __init__(self):
        super().__init__("Conexões")
        self._build_ui()

    def _build_ui(self):
        self.databases = (ConfigService.load_databases())
                
        # Formulário
        form_layout = QFormLayout()
        self.cbo_projeto = QComboBox()
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
        self._projects_map = {}
        
        self.cbo_banco.currentTextChanged.connect(self._on_database_changed)
        self.cbo_projeto.currentIndexChanged.connect(self._on_project_changed)
        self._on_database_changed(self.cbo_banco.currentText())
        
        # Conectar os sinais para a atualização reativa da JDBC URL
        self.txt_host.textChanged.connect(self.update_jdbc_url)
        self.txt_porta.textChanged.connect(self.update_jdbc_url)
        self.txt_database.textChanged.connect(self.update_jdbc_url)
        self.txt_schema.textChanged.connect(self.update_jdbc_url)
        self.txt_usuario.textChanged.connect(self.update_jdbc_url)
        self.txt_password.textChanged.connect(self.update_jdbc_url)
        self.txt_caminho.textChanged.connect(self.update_jdbc_url)
        
        form_layout.addRow(QLabel("Projeto Associado"), self.cbo_projeto)
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

        # BUG FIX: Alteração - Todos os botões devem possuir o mesmo tamanho (tamanho do maior texto)
        self.adjust_button_sizes([self.btn_new, self.btn_save, self.btn_delete, self.btn_test])

        self.tbl_connections = QTableWidget()
        self.current_connection_id = None
        self.configure_table(self.tbl_connections, ["ID", "Projeto", "Conexão", "Banco", "Host", "Porta", "Database", "Schema", "Usuário", "Ativo"])
        self.tbl_connections.itemSelectionChanged.connect(self._on_selection_changed)
        
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
        # BUG FIX: Depreciado - Comportamento anterior que desmarcava o chk_ativo por padrão
        # #self.chk_ativo.setChecked(False)
        self.chk_ativo.setChecked(True)

    def clear_grid(self):
        self.tbl_connections.setRowCount(0)

    def clear_filter(self):
        self.txt_filtro_grid.clear()

    def clear_all(self):
        self.clear_form()
        self.clear_grid()
        self.clear_filter()

    def enable_form(self, enable: bool):
        self.txt_conexao.setEnabled(enable)
        self.cbo_banco.setEnabled(enable)
        self.txt_host.setEnabled(enable)
        self.txt_porta.setEnabled(enable)
        self.txt_database.setEnabled(enable)
        self.txt_schema.setEnabled(enable)
        self.txt_usuario.setEnabled(enable)
        self.txt_password.setEnabled(enable)
        self.txt_caminho.setEnabled(enable)
        self.txt_jdbc_driver.setEnabled(enable)
        self.txt_jdbc_url.setEnabled(enable)
        self.chk_ativo.setEnabled(enable)

    def get_selected_id_conexao(self):
        row = (self.tbl_connections.currentRow())

        if row < 0:
            return None
        item = (self.tbl_connections.item(row, 0))

        if item is None:
            return None

        return int(item.text())
    
    def get_connection(self) -> ConnectionDTO:
        # BUG FIX: Alteração - Retornando objeto ConnectionDTO em vez de dicionário bruto
        try:
            porta_str = self.txt_porta.text().strip()
            porta = int(porta_str) if porta_str else None
        except ValueError:
            porta = None

        return ConnectionDTO(
            id_conexao=self.current_connection_id,
            id_projeto=self.cbo_projeto.currentData(),
            nm_conexao=self.txt_conexao.text(),
            tp_database=self.cbo_banco.currentText(),
            nm_host=self.txt_host.text(),
            nu_porta=porta,
            nm_database=self.txt_database.text(),
            nm_schema=self.txt_schema.text(),
            nm_usuario=self.txt_usuario.text(),
            tx_password=self.txt_password.text(),
            ds_caminho=self.txt_caminho.text(),
            ds_jdbc_driver=self.txt_jdbc_driver.text(),
            ds_jdbc_url=self.txt_jdbc_url.text(),
            fl_ativo=self.chk_ativo.isChecked()
        )
    
    def get_filter_text(self):
        return self.txt_filtro_grid.text().strip()
    
    def set_filter_text(self, text: str):
        self.txt_filtro_grid.setText(text)

    def set_databases(self, databases):
        self.databases = databases
        self.cbo_banco.clear()
        self.cbo_banco.addItem("Selecione o Banco de Dados")
        for database in databases:
            self.cbo_banco.addItem(database["name"])
    
    def set_connection(self, dto: ConnectionDTO):
        self.txt_conexao.setText(dto.nm_conexao or "")
        self.cbo_banco.setCurrentText(dto.tp_database or "")
        self.txt_host.setText(dto.nm_host or "")
        self.txt_porta.setText(str(dto.nu_porta) if dto.nu_porta is not None else "")
        self.txt_database.setText(dto.nm_database or "")
        self.txt_schema.setText(dto.nm_schema or "")
        self.txt_usuario.setText(dto.nm_usuario or "")
        self.txt_password.setText(dto.tx_password or "")
        self.txt_caminho.setText(dto.ds_caminho or "")
        self.txt_jdbc_driver.setText(dto.ds_jdbc_driver or "")
        self.txt_jdbc_url.setText(dto.ds_jdbc_url or "")
        self.chk_ativo.setChecked(dto.fl_ativo)

    def populate_grid(self, connections):
        # BUG FIX: Alteração - Desabilitar temporariamente a ordenação ao popular a grid para evitar desalinhamento de linhas
        self.tbl_connections.setSortingEnabled(False)
        self.tbl_connections.setRowCount(0)
        for row, connection in enumerate(connections):
            self.tbl_connections.insertRow(row)
            self.tbl_connections.setItem(row, 0, QTableWidgetItem(str(connection.id_conexao)))
            
            # BUG FIX: Implementação - Exibir nome do projeto associado usando o mapeamento populado
            project_name = ""
            if connection.id_projeto:
                project = self._projects_map.get(connection.id_projeto)
                if project:
                    project_name = project.nm_projeto
            self.tbl_connections.setItem(row, 1, QTableWidgetItem(project_name))
            self.tbl_connections.setItem(row, 2, QTableWidgetItem(connection.nm_conexao))
            self.tbl_connections.setItem(row, 3, QTableWidgetItem(connection.tp_database))
            self.tbl_connections.setItem(row, 4, QTableWidgetItem(connection.nm_host or ""))
            self.tbl_connections.setItem(row, 5, QTableWidgetItem(str(connection.nu_porta) if connection.nu_porta is not None else ""))
            self.tbl_connections.setItem(row, 6, QTableWidgetItem(connection.nm_database or ""))
            self.tbl_connections.setItem(row, 7, QTableWidgetItem(connection.nm_schema or ""))
            self.tbl_connections.setItem(row, 8, QTableWidgetItem(connection.nm_usuario or ""))
            self.tbl_connections.setItem(row, 9, QTableWidgetItem("Sim" if connection.fl_ativo else "Não"))
        
        # Redimensiona para os conteúdos e adiciona margem
        self.auto_fit_columns(self.tbl_connections)
        
        # BUG FIX: Alteração - Coluna Porta (índice 5) com tamanho fixo correspondente ao tamanho do texto (como na grid de projetos)
        self.tbl_connections.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        self.tbl_connections.setSortingEnabled(True)
    
    
    def load_connection(self, connection):
        self.current_connection_id = connection.id_conexao
        
        # BUG FIX: Implementação - Obter o nome do projeto escrito na coluna Projeto da grid e selecioná-lo no combobox
        row = self.tbl_connections.currentRow()
        project_name = ""
        if row >= 0:
            item_proj = self.tbl_connections.item(row, 1)
            if item_proj:
                project_name = item_proj.text().strip()

        # Selecionar o projeto correto no combobox bloqueando sinais temporariamente para não limpar credenciais
        self.cbo_projeto.blockSignals(True)
        if project_name:
            index = self.cbo_projeto.findText(project_name)
            if index >= 0:
                self.cbo_projeto.setCurrentIndex(index)
            else:
                self.cbo_projeto.setCurrentIndex(0)
        else:
            self.cbo_projeto.setCurrentIndex(0)
        self.cbo_projeto.blockSignals(False)

        self.txt_conexao.setText(connection.nm_conexao or "")
        self.cbo_banco.setCurrentText(connection.tp_database or "")
        self.txt_host.setText(connection.nm_host or "")
        self.txt_porta.setText(str(connection.nu_porta) if connection.nu_porta is not None else "")
        self.txt_database.setText(connection.nm_database or "")
        self.txt_schema.setText(connection.nm_schema or "")
        self.txt_usuario.setText(connection.nm_usuario or "")
        self.txt_password.setText(connection.tx_password or "")
        self.txt_caminho.setText(connection.ds_caminho or "")
        self.txt_jdbc_driver.setText(connection.ds_jdbc_driver or "")
        self.txt_jdbc_url.setText(connection.ds_jdbc_url or "")
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

        default_port = database.get("default_port", 0)
        default_driver = database.get("driver", "")
        default_url = database.get("jdbc_template", "")

        self.txt_porta.setText(str(default_port))
        self.txt_jdbc_driver.setText(str(default_driver))
        self.txt_jdbc_url.setText(str(default_url))

        # Toggling dinâmico de campos baseados em arquivo vs servidor
        is_file_db = database_name.lower() in ("sqlite", "access", "firebird_embedded", "duckdb")
        self.txt_caminho.setEnabled(is_file_db)
        self.txt_host.setEnabled(not is_file_db)
        self.txt_porta.setEnabled(not is_file_db)
        self.txt_database.setEnabled(not is_file_db)
        self.txt_schema.setEnabled(not is_file_db)
        self.txt_usuario.setEnabled(not is_file_db)
        self.txt_password.setEnabled(not is_file_db)

        # BUG FIX: Alteração - Recalcular a URL JDBC ao alterar o banco
        self.update_jdbc_url()

    # BUG FIX: Implementação - Popula o combobox com a lista de projetos ativos e guarda o mapeamento
    def populate_projects_combo(self, projects):
        self.cbo_projeto.blockSignals(True)
        self.cbo_projeto.clear()
        self.cbo_projeto.addItem("Selecione um Projeto", None)
        self._projects_map = {}
        for p in projects:
            self.cbo_projeto.addItem(p.nm_projeto, p.id_projeto)
            self._projects_map[p.id_projeto] = p
        self.cbo_projeto.blockSignals(False)

    # BUG FIX: Implementação - Evento acionado ao alterar o projeto no combobox
    def _on_project_changed(self, index):
        if index <= 0:
            return
        
        project_id = self.cbo_projeto.currentData()
        if not project_id:
            return
            
        project = self._projects_map.get(project_id)
        if not project:
            return
            
        # Preencher campos de acordo com o projeto selecionado
        self.txt_conexao.setText(project.nm_projeto or "")
        self.cbo_banco.setCurrentText(project.tp_database or "")
        self.txt_host.setText(project.nm_host or "")
        self.txt_porta.setText(str(project.nu_porta) if project.nu_porta is not None else "")
        self.txt_schema.setText(project.nm_schema or "")
        
        # Desencadear lógica de visibilidade do banco de dados e recalcular URL
        self._on_database_changed(project.tp_database)

    # BUG FIX: Implementação - Método reativo para montar a URL JDBC dinamicamente de acordo com os inputs
    def update_jdbc_url(self):
        database_name = self.cbo_banco.currentText()
        database = next((db for db in self.databases if db["name"] == database_name), None)
        if not database:
            return
            
        jdbc_template = database.get("jdbc_template", "")
        jdbc_url = (jdbc_template
                    .replace("{host}", self.txt_host.text().strip())
                    .replace("{port}", self.txt_porta.text().strip())
                    .replace("{database}", self.txt_database.text().strip())
                    .replace("{file}", self.txt_caminho.text().strip())
                    .replace("{schema}", self.txt_schema.text().strip())
                    .replace("{user}", self.txt_usuario.text().strip())
                    .replace("{password}", self.txt_password.text().strip()))
                    
        self.txt_jdbc_url.setText(jdbc_url)
