# Artefato:  connection_controller.py


from modules.connections import (
    ConnectionViewModel
)
from modules.connections.connection_validator import (
    ConnectionValidator
)
from infrastructure.database.connection_tester import (
    ConnectionTester
)
from shared.validators import Validator

class ConnectionController:

    def __init__(self, view, viewmodel: ConnectionViewModel, project_service=None):
        self.view = view
        self.viewmodel = viewmodel
        self.project_service = project_service
        self.on_data_changed_callbacks = []
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
        dto = self.view.get_connection()
        validator = ConnectionValidator()
        report = validator.validate(dto)

        if not report.valid:
            self.view.show_validation(report)
            self.view.txt_conexao.setFocus()
            return False

        return True

    def new_connection(self):
        self.view.clear_form()

    def read_connection(self):
        try:
            # BUG FIX: Implementação - Carregar projetos associados no combobox
            self.load_projects()
            connections = (self.viewmodel.read_connection())
            self.view.populate_grid(connections)
        except Exception as ex:
            self.view.show_error_message("Connection Controller - Load", str(ex))
    
    def save_connection(self):
        try:
            if not self.validate_form():
                return

            dto = self.view.get_connection()

            if self.view.current_connection_id:
                self.viewmodel.update_connection(dto)
            else:
                self.viewmodel.create_connection(dto)

            self.view.show_message("Sucesso", "Conexão salva com sucesso.")
            self.read_connection()
            self.view.clear_form()
            for callback in self.on_data_changed_callbacks:
                try:
                    callback()
                except Exception:
                    pass
        except Exception as ex:
            self.view.show_error_message("Connection Controller - Save", str(ex))

    # Excluir
    def delete_connection(self):
        try:
            id_conexao = (self.view.current_connection_id)

            if not id_conexao:
                self.view.show_warning_message("Aviso", "Selecione uma conexão.")
                return

            session = self.viewmodel.service.repository.session
            from modules.settings.setting import Setting

            n_settings = session.query(Setting).filter(Setting.id_conexao == id_conexao).count()

            msg = (
                f"A exclusão desta conexão será realizada em cascata e removerá permanentemente:\n"
                f"- 1 Conexão\n"
                f"- {n_settings} Configuração(ões) associada(s)\n\n"
                f"Deseja continuar com a exclusão?"
            )

            if not self.view.show_question_message("Confirmação de Exclusão em Cascata", msg):
                return

            self.viewmodel.delete_connection(id_conexao)
            self.view.show_message("Sucesso", "Conexão excluída.")
            self.read_connection()
            self.view.clear_form()
            for callback in self.on_data_changed_callbacks:
                try:
                    callback()
                except Exception:
                    pass
        except Exception as ex:
            self.view.show_error_message("Connection Controller - Delete", str(ex))

    def select_connection(self, id_conexao):
        try:
            connection = (self.viewmodel.get_connection_by_id(id_conexao))
            self.view.load_connection(connection)
        except Exception as ex:
            self.view.show_error_message("Connection Controller - Select", str(ex))

    def test_connection(self):
        try:
            porta_str = self.view.txt_porta.text().strip()
            porta = int(porta_str) if porta_str else 0
        except ValueError:
            self.view.show_error_message("Teste Conexão", "Porta deve ser um número inteiro válido.")
            return

        result = (ConnectionTester.test_connection(
                    tp_database=self.view.cbo_banco.currentText(),
                    nm_host=self.view.txt_host.text(),
                    nu_porta=porta,
                    ds_caminho=self.view.txt_caminho.text()
                ))

        if result.success:
            self.view.show_message("Teste Conexão", result.message)
        else:
            self.view.show_error_message("Teste Conexão", result.message)

    # BUG FIX: Implementação - Método para carregar a lista de projetos e repassar para a view
    def load_projects(self):
        if not self.project_service:
            return
        try:
            projects = self.project_service.get_project()
            self.view.populate_projects_combo(projects)
        except Exception as ex:
            self.view.show_error_message("Connection Controller - Load Projects", str(ex))