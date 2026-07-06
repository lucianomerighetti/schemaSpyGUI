# project_controller.py

from PyQt6.QtWidgets import (
    QMessageBox
)
from modules.projects import (
    ProjectViewModel
)
from shared.validators import Validator

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
        result = Validator.validate(
                Validator.required(self.view.txt_projeto.text(), "o Nome do Projeto"),
                Validator.required(self.view.cbo_banco.currentText(), "o Banco"),
                Validator.required(self.view.txt_host.text(), "o Host"),
                Validator.required(self.view.txt_schema.text(), "o Schema")
            )

        if not result.valid:
            QMessageBox.warning(self.view, "Validação", result.message)
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
            QMessageBox.critical(self.view, "Project Controller - Load", str(ex))

    def save_project(self):
        try:
            if not self.validate_form():
                return

            if self.view.current_project_id:
                self.viewmodel.update_project(
                    id_projeto=self.view.current_project_id,
                    nm_projeto=self.view.txt_projeto.text(),
                    tp_database=self.view.cbo_banco.currentText(),
                    nm_host=self.view.txt_host.text(),
                    nm_schema=self.view.txt_schema.text(),
                    nu_porta=int(self.view.txt_porta.text()) if self.view.txt_porta.text() else 0
                )            
            else:                
                self.viewmodel.create_project(
                    nm_projeto=self.view.txt_projeto.text(),
                    tp_database=self.view.cbo_banco.currentText(),
                    nm_host=self.view.txt_host.text(),
                    nm_schema=self.view.txt_schema.text(),
                    nu_porta=int(self.view.txt_porta.text()) if self.view.txt_porta.text() else 0
                )
            
            QMessageBox.information(self.view, "Sucesso", "Projeto salvo com sucesso.")
            
            self.read_project()
            self.view.clear_form()
        except Exception as ex:
            QMessageBox.critical(self.view, "Project Controller - Save", str(ex))

    def delete_project(self):
        try:
            id_projeto = (self.view.get_selected_id_projeto())
            if not id_projeto:
                QMessageBox.warning(self.view, "Aviso", "Selecione um projeto.")
                return

            confirm = QMessageBox.question(self.view, "Confirmação", "Deseja excluir o projeto?")

            if (confirm != QMessageBox.StandardButton.Yes):
                return

            self.viewmodel.delete_project(id_projeto)

            QMessageBox.information(self.view, "Sucesso", "Projeto excluído.")

            self.read_project()
            self.view.clear_form()

        except Exception as ex:
            QMessageBox.critical(self.view, "Project Controller - Delete", str(ex))

    def select_project(self, id_projeto):
        try:
            project = (self.viewmodel.get_project_by_id(id_projeto))
            self.view.load_project(project)
        except Exception as ex:
            QMessageBox.critical(self.view, "Project Controller - Select", str(ex))
