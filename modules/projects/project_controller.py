# Artefato:  project_controller.py

import json
from PyQt6.QtWidgets import QFileDialog
from .project_viewmodel import ProjectViewModel
from .project_dto import ProjectDTO
from .import_dialog import ImportProjectsDialog
from .project_validator import ProjectValidator

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
        self.view.btn_import.clicked.connect(self.import_projects)
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

    # BUG FIX: Implementação - Método de importação em lote a partir do diálogo modal
    def import_projects(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self.view,
                "Importar Projetos (JSON)",
                "",
                "Arquivos JSON (*.json)"
            )
            if not file_path:
                return

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                data = [data]

            if not isinstance(data, list):
                self.view.show_error_message("Erro de Formato", "O arquivo JSON deve conter um projeto ou uma lista de projetos.")
                return

            dialog = ImportProjectsDialog(data, parent=self.view)
            if dialog.exec() == ImportProjectsDialog.DialogCode.Accepted:
                imported_items = dialog.get_imported_projects()
                
                success_count = 0
                for item in imported_items:
                    dto = ProjectDTO(
                        nm_projeto=item["nm_projeto"],
                        tp_database=item["tp_database"],
                        nm_database=item["nm_database"],
                        nm_host=item["nm_host"],
                        nm_schema=item["nm_schema"],
                        nu_porta=item["nu_porta"]
                    )
                    self.viewmodel.create_project(dto)
                    success_count += 1
                
                self.view.show_message("Sucesso", f"{success_count} projeto(s) importado(s) com sucesso.")
                self.read_project()
                self.view.clear_form()

        except Exception as ex:
            self.view.show_error_message("Project Controller - Import", str(ex))
