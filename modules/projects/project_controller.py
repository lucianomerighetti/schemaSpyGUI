# Artefato:  project_controller.py

from modules.projects import (
    ProjectViewModel
)
from modules.projects.project_validator import (
    ProjectValidator
)

class ProjectController:

    def __init__(self, view, viewmodel: ProjectViewModel):
        self.view = view
        self.viewmodel = viewmodel
        self._connect_signals()
        self.read_project()

    def _connect_signals(self):
        # Botões
        self.view.btn_new.clicked.connect(self.new_project)
        self.view.btn_save.clicked.connect(self.save_project)
        self.view.btn_delete.clicked.connect(self.delete_project)
        # Seleção da Grid
        self.view.project_selected.connect(self.select_project)
    
    def validate_form(self):
        dto = self.view.get_project()
        validator = ProjectValidator()
        report = validator.validate(dto)

        if not report.valid:
            self.view.show_validation(report)
            self.view.txt_projeto.setFocus()
            return False

        return True

    def new_project(self):
        self.view.clear_form()

    def read_project(self):
        try:
            project = (self.viewmodel.read_project())
            self.view.populate_grid(project)
        except Exception as ex:
            self.view.show_error_message("Project Controller - Load", str(ex))

    def save_project(self):
        try:
            if not self.validate_form():
                return

            dto = self.view.get_project()

            if self.view.current_project_id:
                self.viewmodel.update_project(dto)            
            else:                
                self.viewmodel.create_project(dto)
            
            self.view.show_message("Sucesso", "Projeto salvo com sucesso.")
            
            self.read_project()
            self.view.clear_form()
        except Exception as ex:
            self.view.show_error_message("Project Controller - Save", str(ex))

    def delete_project(self):
        try:
            id_projeto = (self.view.get_selected_id_projeto())
            if not id_projeto:
                self.view.show_warning_message("Aviso", "Selecione um projeto.")
                return

            if not self.view.show_question_message("Confirmação", "Deseja excluir o projeto?"):
                return

            self.viewmodel.delete_project(id_projeto)

            self.view.show_message("Sucesso", "Projeto excluído.")

            self.read_project()
            self.view.clear_form()

        except Exception as ex:
            self.view.show_error_message("Project Controller - Delete", str(ex))

    def select_project(self, id_projeto):
        try:
            project = (self.viewmodel.get_project_by_id(id_projeto))
            self.view.load_project(project)
        except Exception as ex:
            self.view.show_error_message("Project Controller - Select", str(ex))
