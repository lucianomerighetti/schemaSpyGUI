# settings_view.py
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QCheckBox,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
    QTabWidget,
    QGroupBox,
    QTextEdit,
    QHeaderView,
    QFileDialog,
    QGridLayout
)
from PyQt6.QtCore import pyqtSignal, Qt
from shared.views.base_view import BaseView
from .setting_dto import SettingDTO

class SettingView(BaseView):
    setting_selected = pyqtSignal(int)
    view_shown = pyqtSignal()

    def __init__(self):
        super().__init__("Configurações")
        self.current_setting_id = None
        self._connections_map = {}
        self._build_ui()

    def _build_ui(self):
        # QTabWidget principal
        self.tabs = QTabWidget()
        
        # --- ABA 1: GRID ---
        self.grid_tab = QWidget()
        grid_layout = QVBoxLayout(self.grid_tab)
        self.tbl_settings = QTableWidget()
        self.configure_table(self.tbl_settings, ["ID", "Nome Configuração", "Conexão", "Pasta de Output"])
        self.tbl_settings.itemSelectionChanged.connect(self._on_selection_changed)
        grid_layout.addWidget(self.tbl_settings)
        self.tabs.addTab(self.grid_tab, "Lista de Configurações")

        # --- ABA 2: PARAMETERS & FLAGS ---
        self.params_tab = QWidget()
        params_layout = QVBoxLayout(self.params_tab)
        
        # Formulário de Conexão Geral
        db_group = QGroupBox("Parâmetros de Execução do SchemaSpy")
        db_form = QFormLayout(db_group)
        
        self.txt_nm_setting = QLineEdit()
        self.txt_nm_setting.setPlaceholderText("Ex: Configuração de Produção Oracle")
        
        self.cbo_conexao = QComboBox()
        
        # Drivers, SchemaSpy e Properties com seletores de arquivo
        self.txt_db_driver_path = QLineEdit()
        self.btn_db_driver_path = QPushButton("Escolher")
        self.btn_db_driver_path.clicked.connect(lambda: self._choose_file(self.txt_db_driver_path, "Drivers JDBC (*.jar);;Todos os arquivos (*)"))
        
        driver_layout = QHBoxLayout()
        driver_layout.addWidget(self.txt_db_driver_path)
        driver_layout.addWidget(self.btn_db_driver_path)

        self.txt_schemaspy_path = QLineEdit()
        self.btn_schemaspy_path = QPushButton("Escolher")
        self.btn_schemaspy_path.clicked.connect(lambda: self._choose_file(self.txt_schemaspy_path, "SchemaSpy Executável (*.jar);;Todos os arquivos (*)"))
        
        schemaspy_layout = QHBoxLayout()
        schemaspy_layout.addWidget(self.txt_schemaspy_path)
        schemaspy_layout.addWidget(self.btn_schemaspy_path)

        self.txt_properties_path = QLineEdit()
        self.btn_properties_path = QPushButton("Escolher")
        self.btn_properties_path.clicked.connect(lambda: self._choose_file(self.txt_properties_path, "Arquivos de Propriedades (*.properties);;Todos os arquivos (*)"))
        
        properties_path_layout = QHBoxLayout()
        properties_path_layout.addWidget(self.txt_properties_path)
        properties_path_layout.addWidget(self.btn_properties_path)

        self.txt_properties_text = QLineEdit()

        db_form.addRow(QLabel("Conexão Associada:"), self.cbo_conexao)
        db_form.addRow(QLabel("Nome Configuração:"), self.txt_nm_setting)
        db_form.addRow(QLabel("Path to DB Driver (-dp):"), driver_layout)
        db_form.addRow(QLabel("Path to SchemaSpy jar:"), schemaspy_layout)
        db_form.addRow(QLabel("Properties Path:"), properties_path_layout)
        db_form.addRow(QLabel("Properties:"), self.txt_properties_text)

        # Painéis inferiores de Qualidade e Flags
        bottom_params_layout = QHBoxLayout()
        
        quality_group = QGroupBox("Qualidade de Imagens")
        quality_vbox = QVBoxLayout(quality_group)
        self.chk_high_quality = QCheckBox("High Quality")
        self.chk_low_quality = QCheckBox("Low Quality")
        quality_vbox.addWidget(self.chk_high_quality)
        quality_vbox.addWidget(self.chk_low_quality)
        quality_vbox.addStretch()
        
        flags_group = QGroupBox("Flags gerais do SchemaSpy")
        flags_grid = QHBoxLayout(flags_group)
        
        col1 = QVBoxLayout()
        self.chk_a_html = QCheckBox("aHTML")
        self.chk_no_rows = QCheckBox("noRows")
        self.chk_rails = QCheckBox("rails")
        col1.addWidget(self.chk_a_html)
        col1.addWidget(self.chk_no_rows)
        col1.addWidget(self.chk_rails)
        
        col2 = QVBoxLayout()
        self.chk_no_html = QCheckBox("noHTML")
        self.chk_dinc_fk = QCheckBox("dincFK")
        self.chk_single_sign_on = QCheckBox("Single Sign-On (-sso)")
        self.chk_single_sign_on.setEnabled(False)
        col2.addWidget(self.chk_no_html)
        col2.addWidget(self.chk_dinc_fk)
        col2.addWidget(self.chk_single_sign_on)

        col3 = QVBoxLayout()
        self.chk_no_logo = QCheckBox("noLogo")
        self.chk_no_ads = QCheckBox("noAds")
        self.chk_show_finish = QCheckBox("Show Output when finished")
        col3.addWidget(self.chk_no_logo)
        col3.addWidget(self.chk_no_ads)
        col3.addWidget(self.chk_show_finish)

        flags_grid.addLayout(col1)
        flags_grid.addLayout(col2)
        flags_grid.addLayout(col3)

        bottom_params_layout.addWidget(quality_group, 1)
        bottom_params_layout.addWidget(flags_group, 2)

        params_layout.addWidget(db_group)
        params_layout.addLayout(bottom_params_layout)
        params_layout.addStretch()
        self.tabs.addTab(self.params_tab, "Parameters / Flags")

        # --- ABA 3: OUTPUT OPTIONS ---
        self.output_tab = QWidget()
        output_layout = QVBoxLayout(self.output_tab)
        
        options_group = QGroupBox("Opções de Geração e Filtros")
        options_form = QFormLayout(options_group)
        
        self.txt_output_dir = QLineEdit()
        self.btn_output_dir = QPushButton("Escolher")
        self.btn_output_dir.clicked.connect(lambda: self._choose_dir(self.txt_output_dir))
        
        output_dir_layout = QHBoxLayout()
        output_dir_layout.addWidget(self.txt_output_dir)
        output_dir_layout.addWidget(self.btn_output_dir)

        self.txt_schema_explore = QLineEdit()
        self.chk_all_schemas = QCheckBox("All Schemas")
        self.chk_all_schemas.stateChanged.connect(self._on_all_schemas_changed)

        schema_layout = QHBoxLayout()
        schema_layout.addWidget(self.txt_schema_explore)
        schema_layout.addWidget(self.chk_all_schemas)

        self.txt_meta_file_path = QLineEdit()
        self.btn_meta_file_path = QPushButton("Escolher")
        self.btn_meta_file_path.clicked.connect(lambda: self._choose_file(self.txt_meta_file_path, "Metafiles XML (*.xml);;Todos os arquivos (*)"))

        meta_layout = QHBoxLayout()
        meta_layout.addWidget(self.txt_meta_file_path)
        meta_layout.addWidget(self.btn_meta_file_path)

        self.txt_description = QTextEdit()
        self.txt_description.setMaximumHeight(80)

        self.txt_table_name_regex = QLineEdit()
        self.txt_table_exclusion_regex = QLineEdit()
        self.txt_column_exclusion_regex = QLineEdit()
        self.chk_excluded_relationships = QCheckBox("Excluded relationships")

        options_form.addRow(QLabel("Output Directory (-o):"), output_dir_layout)
        options_form.addRow(QLabel("Schema/s to explore (-s):"), schema_layout)
        options_form.addRow(QLabel("Metafile Path (-meta):"), meta_layout)
        options_form.addRow(QLabel("Description on summary (-desc):"), self.txt_description)
        options_form.addRow(QLabel("Table Name RegExp (-i):"), self.txt_table_name_regex)
        options_form.addRow(QLabel("Table Exclusion RegExp (-I):"), self.txt_table_exclusion_regex)
        options_form.addRow(QLabel("Column Exclusion RegExp (-x):"), self.txt_column_exclusion_regex)
        options_form.addRow(QLabel(""), self.chk_excluded_relationships)

        # Style Group Box
        style_group = QGroupBox(" Style: (Modify the .css to specify HTML fonts) ")
        style_grid = QGridLayout(style_group)
        
        self.cbo_charset = QComboBox()
        self.cbo_charset.setEditable(True)
        self.cbo_charset.addItems(["", "UTF-8", "ISO-8859-1", "ISO-8859-2", "ISO-8859-3", "ISO-8859-4", "ISO-8859-5", "ISO-8859-6", "ISO-8859-7", "ISO-8859-8", "ISO-8859-9", "ISO-8859-10", "ISO-8859-11", "ISO-8859-12", "ISO-8859-13", "ISO-8859-14", "ISO-8859-15"])
        
        self.txt_font_name = QLineEdit()
        self.txt_font_size = QLineEdit()
        
        self.txt_css_path = QLineEdit()
        self.btn_css_path = QPushButton("Escolher")
        self.btn_css_path.clicked.connect(lambda: self._choose_file(self.txt_css_path, "Arquivos CSS (*.css);;Todos os arquivos (*)"))

        css_layout = QHBoxLayout()
        css_layout.addWidget(self.txt_css_path)
        css_layout.addWidget(self.btn_css_path)

        style_grid.addWidget(QLabel("Charset (-charset):"), 0, 0)
        style_grid.addWidget(self.cbo_charset, 0, 1)
        style_grid.addWidget(QLabel("Font Name (-font):"), 0, 2)
        style_grid.addWidget(self.txt_font_name, 0, 3)
        style_grid.addWidget(QLabel("Font size (-fontsize):"), 0, 4)
        style_grid.addWidget(self.txt_font_size, 0, 5)
        style_grid.addWidget(QLabel("Style CSS file (-css):"), 1, 0)
        style_grid.addLayout(css_layout, 1, 1, 1, 5)

        output_layout.addWidget(options_group)
        output_layout.addWidget(style_group)
        output_layout.addStretch()
        self.tabs.addTab(self.output_tab, "Output Options")

        # Adicionar QTabWidget na visualização principal
        self.content_layout.addWidget(self.tabs)

        # Botões Globais de CRUD
        button_layout = QHBoxLayout()
        self.btn_new = QPushButton("Novo")
        self.btn_save = QPushButton("Salvar")
        self.btn_delete = QPushButton("Excluir")
        button_layout.addWidget(self.btn_new)
        button_layout.addWidget(self.btn_save)
        button_layout.addWidget(self.btn_delete)
        button_layout.addStretch()
        self.adjust_button_sizes([self.btn_new, self.btn_save, self.btn_delete])

        self.content_layout.addLayout(button_layout)

    def _choose_file(self, line_edit, filter_str):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo", "", filter_str)
        if file_path:
            line_edit.setText(file_path)

    def _choose_dir(self, line_edit):
        dir_path = QFileDialog.getExistingDirectory(self, "Selecionar Diretório", "")
        if dir_path:
            line_edit.setText(dir_path)

    def _on_all_schemas_changed(self, state):
        is_checked = (state == 2 or state == Qt.CheckState.Checked)
        self.txt_schema_explore.setEnabled(not is_checked)

    def _on_selection_changed(self):
        row = self.tbl_settings.currentRow()
        if row < 0:
            return
        item = self.tbl_settings.item(row, 0)
        if item is None:
            return
        self.setting_selected.emit(int(item.text()))

    def get_selected_id_setting(self):
        row = self.tbl_settings.currentRow()
        if row < 0:
            return None
        item = self.tbl_settings.item(row, 0)
        if item is None:
            return None
        return int(item.text())

    def populate_connections_combo(self, connections):
        self.cbo_conexao.blockSignals(True)
        self.cbo_conexao.clear()
        self.cbo_conexao.addItem("Selecione uma Conexão", None)
        self._connections_map = {}
        for conn in connections:
            self.cbo_conexao.addItem(conn.nm_conexao, conn.id_conexao)
            self._connections_map[conn.id_conexao] = conn
        self.cbo_conexao.blockSignals(False)

    def clear_form(self):
        self.current_setting_id = None
        self.txt_nm_setting.clear()
        self.cbo_conexao.setCurrentIndex(0)
        self.txt_db_driver_path.clear()
        self.txt_schemaspy_path.clear()
        self.txt_properties_path.clear()
        self.txt_properties_text.clear()
        self.chk_high_quality.setChecked(False)
        self.chk_low_quality.setChecked(False)
        self.chk_a_html.setChecked(False)
        self.chk_no_html.setChecked(False)
        self.chk_dinc_fk.setChecked(False)
        self.chk_no_ads.setChecked(False)
        self.chk_no_logo.setChecked(False)
        self.chk_no_rows.setChecked(False)
        self.chk_rails.setChecked(False)
        self.chk_show_finish.setChecked(False)
        
        self.txt_output_dir.clear()
        self.txt_schema_explore.clear()
        self.txt_schema_explore.setEnabled(True)
        self.chk_all_schemas.setChecked(False)
        self.txt_meta_file_path.clear()
        self.txt_description.clear()
        self.txt_table_name_regex.clear()
        self.txt_table_exclusion_regex.clear()
        self.txt_column_exclusion_regex.clear()
        self.chk_excluded_relationships.setChecked(False)
        self.cbo_charset.setCurrentIndex(0)
        self.txt_font_name.clear()
        self.txt_font_size.clear()
        self.txt_css_path.clear()
        
        self.tabs.setCurrentIndex(1)

    def populate_grid(self, settings):
        self.tbl_settings.setSortingEnabled(False)
        self.tbl_settings.setRowCount(0)
        for row, s in enumerate(settings):
            self.tbl_settings.insertRow(row)
            self.tbl_settings.setItem(row, 0, QTableWidgetItem(str(s.id_setting)))
            self.tbl_settings.setItem(row, 1, QTableWidgetItem(s.nm_setting))
            
            conn_name = ""
            if s.id_conexao:
                conn = self._connections_map.get(s.id_conexao)
                if conn:
                    conn_name = conn.nm_conexao
            
            self.tbl_settings.setItem(row, 2, QTableWidgetItem(conn_name))
            self.tbl_settings.setItem(row, 3, QTableWidgetItem(s.output_dir or ""))
        
        self.auto_fit_columns(self.tbl_settings)
        self.tbl_settings.setSortingEnabled(True)

    def get_setting(self) -> SettingDTO:
        return SettingDTO(
            id_setting=self.current_setting_id,
            nm_setting=self.txt_nm_setting.text(),
            id_conexao=self.cbo_conexao.currentData(),
            db_driver_path=self.txt_db_driver_path.text(),
            schemaspy_path=self.txt_schemaspy_path.text(),
            properties_path=self.txt_properties_path.text(),
            properties_text=self.txt_properties_text.text(),
            high_quality=self.chk_high_quality.isChecked(),
            low_quality=self.chk_low_quality.isChecked(),
            single_sign_on=self.chk_single_sign_on.isChecked(),
            show_finish=self.chk_show_finish.isChecked(),
            a_html=self.chk_a_html.isChecked(),
            no_html=self.chk_no_html.isChecked(),
            dinc_fk=self.chk_dinc_fk.isChecked(),
            no_ads=self.chk_no_ads.isChecked(),
            no_logo=self.chk_no_logo.isChecked(),
            no_rows=self.chk_no_rows.isChecked(),
            rails=self.chk_rails.isChecked(),
            output_dir=self.txt_output_dir.text(),
            schema_explore=self.txt_schema_explore.text(),
            all_schemas=self.chk_all_schemas.isChecked(),
            meta_file_path=self.txt_meta_file_path.text(),
            description=self.txt_description.toPlainText(),
            table_name_regex=self.txt_table_name_regex.text(),
            table_exclusion_regex=self.txt_table_exclusion_regex.text(),
            column_exclusion_regex=self.txt_column_exclusion_regex.text(),
            excluded_relationships=self.chk_excluded_relationships.isChecked(),
            charset=self.cbo_charset.currentText().strip(),
            font_name=self.txt_font_name.text(),
            font_size=self.txt_font_size.text(),
            css_path=self.txt_css_path.text()
        )

    def load_setting(self, s):
        self.current_setting_id = s.id_setting
        self.txt_nm_setting.setText(s.nm_setting or "")
        
        self.cbo_conexao.blockSignals(True)
        index = self.cbo_conexao.findData(s.id_conexao)
        if index >= 0:
            self.cbo_conexao.setCurrentIndex(index)
        else:
            self.cbo_conexao.setCurrentIndex(0)
        self.cbo_conexao.blockSignals(False)

        self.txt_db_driver_path.setText(s.db_driver_path or "")
        self.txt_schemaspy_path.setText(s.schemaspy_path or "")
        self.txt_properties_path.setText(s.properties_path or "")
        self.txt_properties_text.setText(s.properties_text or "")
        self.chk_high_quality.setChecked(s.high_quality)
        self.chk_low_quality.setChecked(s.low_quality)
        self.chk_a_html.setChecked(s.a_html)
        self.chk_no_html.setChecked(s.no_html)
        self.chk_dinc_fk.setChecked(s.dinc_fk)
        self.chk_no_ads.setChecked(s.no_ads)
        self.chk_no_logo.setChecked(s.no_logo)
        self.chk_no_rows.setChecked(s.no_rows)
        self.chk_rails.setChecked(s.rails)
        self.chk_show_finish.setChecked(s.show_finish)
        
        self.txt_output_dir.setText(s.output_dir or "")
        self.txt_schema_explore.setText(s.schema_explore or "")
        self.chk_all_schemas.setChecked(s.all_schemas)
        self.txt_meta_file_path.setText(s.meta_file_path or "")
        self.txt_description.setPlainText(s.description or "")
        self.txt_table_name_regex.setText(s.table_name_regex or "")
        self.txt_table_exclusion_regex.setText(s.table_exclusion_regex or "")
        self.txt_column_exclusion_regex.setText(s.column_exclusion_regex or "")
        self.chk_excluded_relationships.setChecked(s.excluded_relationships)
        self.cbo_charset.setCurrentText(s.charset or "")
        self.txt_font_name.setText(s.font_name or "")
        self.txt_font_size.setText(s.font_size or "")
        self.txt_css_path.setText(s.css_path or "")
        
        self.tabs.setCurrentIndex(1)

    def showEvent(self, event):
        super().showEvent(event)
        self.view_shown.emit()