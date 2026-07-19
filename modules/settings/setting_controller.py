# setting_controller.py
from .setting_validator import SettingValidator
from .setting_dto import SettingDTO

class SettingController:
    def __init__(self, view, viewmodel, connection_service=None):
        self.view = view
        self.viewmodel = viewmodel
        self.connection_service = connection_service
        self._connect_signals()
        self.read_setting()

    def _connect_signals(self):
        self.view.btn_new.clicked.connect(self.new_setting)
        self.view.btn_save.clicked.connect(self.save_setting)
        self.view.btn_delete.clicked.connect(self.delete_setting)
        self.view.setting_selected.connect(self.select_setting)
        self.view.view_shown.connect(self.read_setting)

    def validate_form(self):
        dto = self.view.get_setting()
        validator = SettingValidator()
        report = validator.validate(dto)

        if not report.valid:
            self.view.show_validation(report)
            return False

        return True

    def new_setting(self):
        self.view.clear_form()

    def load_connections(self):
        if self.connection_service:
            try:
                connections = self.connection_service.get_connection()
                self.view.populate_connections_combo(connections)
            except Exception as ex:
                self.view.show_error_message("Setting Controller - Load Connections", str(ex))

    def read_setting(self):
        try:
            self.load_connections()
            settings = self.viewmodel.read_setting()
            self.view.populate_grid(settings)
        except Exception as ex:
            self.view.show_error_message("Setting Controller - Load Settings", str(ex))

    def save_setting(self):
        try:
            if not self.validate_form():
                return

            dto = self.view.get_setting()

            if self.view.current_setting_id:
                self.viewmodel.update_setting(dto)
            else:
                self.viewmodel.create_setting(dto)

            self.view.show_message("Sucesso", "Configuração salva com sucesso.")
            self.read_setting()
            self.view.clear_form()
        except Exception as ex:
            self.view.show_error_message("Setting Controller - Save", str(ex))

    def delete_setting(self):
        try:
            id_setting = self.view.get_selected_id_setting()
            if not id_setting:
                self.view.show_warning_message("Aviso", "Selecione uma configuração.")
                return

            if not self.view.show_question_message("Confirmação", "Deseja excluir a configuração?"):
                return

            self.viewmodel.delete_setting(id_setting)
            self.view.show_message("Sucesso", "Configuração excluída.")
            self.read_setting()
            self.view.clear_form()
        except Exception as ex:
            self.view.show_error_message("Setting Controller - Delete", str(ex))

    def select_setting(self, id_setting):
        try:
            setting = self.viewmodel.get_setting_by_id(id_setting)
            if setting:
                self.view.load_setting(setting)
        except Exception as ex:
            self.view.show_error_message("Setting Controller - Select", str(ex))
