# Artefato:  project_viewmodel.py

from shared.viewmodels.base_viewmodel import BaseViewModel
from .project_dto import ProjectDTO

class ProjectViewModel(BaseViewModel):

    def __init__(self, service):
        super().__init__()
        self.service = service
    
    def get_project_by_id(self, id_projeto):
        return self.service.get_project_by_id(id_projeto)
    
    def create_project(self, dto: ProjectDTO):
        return self.service.create_project(dto)

    def read_project(self):
        return self.service.get_project()

    def update_project(self, dto: ProjectDTO):
        return self.service.update_project(dto)
    
    def delete_project(self, id_projeto: int):
        return self.service.delete_project(id_projeto)

    def get_project_by_name(self, nm_projeto: str):
        return self.service.get_project_by_name(nm_projeto)
