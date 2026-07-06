# project_viewmodel.py

from shared.viewmodels.base_viewmodel import BaseViewModel

class ProjectViewModel(BaseViewModel):

    def __init__(self, service):
        super().__init__()
        self.service = service
    
    def get_project_by_id(self, id_projeto):
        return self.service.get_project_by_id(id_projeto)
    
    def create_project(
        self,
        nm_projeto,
        tp_database,
        nm_host,
        nm_schema,
        nu_porta
    ):
        return self.service.create_project(
            nm_projeto,
            tp_database,
            nm_host,
            nm_schema,
            nu_porta
        )

    def read_project(self):
        return self.service.get_project()

    def update_project(
        self,
        id_projeto,
        nm_projeto,
        tp_database,
        nm_host,
        nm_schema,
        nu_porta
    ):
        return self.service.update_project(
            id_projeto,
            nm_projeto,
            tp_database,
            nm_host,
            nm_schema,
            nu_porta
        )
    
    def delete_project(self, id_projeto: int):
        return self.service.delete_project(id_projeto)
