# connection_controller.py

from PyQt6.QtWidgets import (
    QMessageBox
)
from modules.connections import (
    ConnectionViewModel
)
from infrastructure.database.connection_tester import (
    ConnectionTester
)
from shared.validators import Validator

class ConnectionController:

    def __init__(self, view, viewmodel: ConnectionViewModel):
        self.view = view
        self.viewmodel = viewmodel
        self._connect_signals()
        self.read_connection()

    def _connect_signals(self):
        # Botões
        self.view.btn_new.clicked.connect(self.new_connection)
        self.view.btn_save.clicked.connect(self.save_connection)
        self.view.btn_delete.clicked.connect(self.delete_connection)
        self.view.btn_test.clicked.connect(self.test_connection)
        # Seleção da Grid
        self.view.connection_selected.connect(self.select_connection)
    
    def validate_form(self):
        result = Validator.validate(
            Validator.required(self.view.txt_conexao.text(), "a Conexão"),
            Validator.required(self.view.cbo_banco.currentText(), "o Banco"),
            Validator.required(self.view.txt_host.text(), "o Host"),
            Validator.required(self.view.txt_porta.text(), "a Porta"),
            Validator.required(self.view.txt_database.text(), "o Database"),
            Validator.required(self.view.txt_schema.text(), "o Schema"),
            Validator.required(self.view.txt_usuario.text(), "o Usuário"),
            Validator.required(self.view.txt_password .text(), "a Senha"),
            Validator.required(self.view.txt_caminho.text(), "o Caminho"),
            Validator.required(self.view.txt_jdbc_driver.text(), "o JDBC Driver"),
            Validator.required(self.view.txt_jdbc_url.text(), "o JDBC URL")
        )

        if not result.valid:
            QMessageBox.warning(self.view, "Validação", result.message)
            self.view.txt_conexao.setFocus()
            return False

        return True

    def new_connection(self):
        self.view.clear_form()

    def read_connection(self):
        try:
            connections = (self.viewmodel.read_connection())
            self.view.populate_grid(connections)
        except Exception as ex:
            QMessageBox.critical(self.view, "Connection Controller - Load", str(ex))
    
    def save_connection(self):
        try:
            if not self.validate_form():
                return

            if self.view.current_connection_id:
                self.viewmodel.update_connection(
                    id_conexao=self.view.current_connection_id,
                    nm_conexao=self.view.txt_conexao.text(),
                    tp_database=self.view.cbo_banco.currentText(),
                    nm_host=self.view.txt_host.text(),
                    nu_porta=int(self.view.txt_porta.text()) if self.view.txt_porta.text() else 0,
                    nm_database=self.view.txt_database.text(),
                    nm_schema=self.view.txt_schema.text(),
                    nm_usuario=self.view.txt_usuario.text(),
                    tx_password=self.view.txt_password.text(),
                    ds_caminho=self.view.txt_caminho.text(),
                    ds_jdbc_driver=self.view.txt_jdbc_driver.text(),
                    ds_jdbc_url=self.view.txt_jdbc_url.text(),
                    fl_ativo=self.view.chk_ativo.isChecked()
                )
            else:
                self.viewmodel.create_connection(
                    nm_conexao=self.view.txt_conexao.text(),
                    tp_database=self.view.cbo_banco.currentText(),
                    nm_host=self.view.txt_host.text(),
                    nu_porta=int(self.view.txt_porta.text()) if self.view.txt_porta.text() else 0,
                    nm_database=self.view.txt_database.text(),
                    nm_schema=self.view.txt_schema.text(),
                    nm_usuario=self.view.txt_usuario.text(),
                    tx_password=self.view.txt_password.text(),
                    ds_caminho=self.view.txt_caminho.text(),
                    ds_jdbc_driver=self.view.txt_jdbc_driver.text(),
                    ds_jdbc_url=self.view.txt_jdbc_url.text(),
                    fl_ativo=self.view.chk_ativo.isChecked()
                )

            QMessageBox.information(self.view, "Sucesso", "Conexão salva com sucesso.")
            self.read_connection()
            self.view.clear_form()
        except Exception as ex:
            QMessageBox.critical(self.view, "Connection Controller - Save", str(ex))

    # Excluir
    def delete_connection(self):
        try:
            id_conexao = (self.view.current_connection_id)

            if not id_conexao:
                QMessageBox.warning(self.view, "Aviso", "Selecione uma conexão.")
                return

            self.viewmodel.delete_connection(id_conexao)
            QMessageBox.information(self.view, "Sucesso", "Conexão excluída.")
            self.read_connection()
            self.view.clear_form()
        except Exception as ex:
            QMessageBox.critical(self.view, "Connection Controller - Delete", str(ex))

    def select_connection(self, id_conexao):
        try:
            connection = (self.viewmodel.get_connection_by_id(id_conexao))
            self.view.load_connection(connection)
        except Exception as ex:
            QMessageBox.critical(self.view, "Connection Controller - Select", str(ex))

    def test_connection(self):
        result = (ConnectionTester.test_connection(
                    tp_database=self.view.cbo_banco.currentText(),
                    nm_host=self.view.txt_host.text(),
                    nu_porta=int(self.view.txt_porta.text())
                    if self.view.txt_porta.text() else 0,
                    ds_caminho=self.view.txt_caminho.text()
                ))

        if result.success:
            QMessageBox.information(self.view, "Teste Conexão", result.message)
        else:
            QMessageBox.critical(self.view, "Teste Conexão", result.message)