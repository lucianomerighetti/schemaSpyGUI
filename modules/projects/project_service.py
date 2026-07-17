# Artefato:  project_service.py
from shared.services.base_service import (
    BaseService
)
from modules.projects import (
    Project,
    ProjectRepository
)
from .project_dto import ProjectDTO

class ProjectService(BaseService):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def get_project(self):
        return self.repository.get_all()

    def info_project(self, name: str):
        self.validate_required(name, "Nome do Projeto")
        self.info(f"Criando projeto: {name}")

    def create_project(self, dto: ProjectDTO):
        project = Project(
            nm_projeto=dto.nm_projeto,
            tp_database=dto.tp_database,
            nm_host=dto.nm_host,
            nm_schema=dto.nm_schema,
            nu_porta=dto.nu_porta
        )
        return self.repository.create(project)

    def update_project(self, dto: ProjectDTO):
        project = (self.repository.get_by_id(dto.id_projeto))

        if not project:
            raise Exception("Projeto não encontrado.")

        project.nm_projeto = dto.nm_projeto
        project.tp_database = dto.tp_database
        project.nm_host = dto.nm_host
        project.nm_schema = dto.nm_schema
        project.nu_porta = dto.nu_porta

        self.repository.update()
        
    def delete_project(self, id_projeto: int):
        project = (self.repository.get_by_id(id_projeto))
        if not project:
            raise Exception("Projeto não encontrado.")
        self.repository.delete(project)
        
    def get_project_by_id(self, id_projeto):
        return self.repository.get_by_id(id_projeto)
