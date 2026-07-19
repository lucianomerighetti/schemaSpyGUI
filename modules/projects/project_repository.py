# project_repository.py

from sqlalchemy.orm import Session
from modules.projects import (
    Project
)
class ProjectRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return (
            self.session
            .query(Project)
            .order_by(Project.nm_projeto)
            .all()
        )

    def get_by_id(self, id_projeto: int):
        return (
            self.session
            .query(Project)
            .filter(Project.id_projeto == id_projeto)
            .first()
        )
        
    def create(self, project: Project):
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    def update(self):
        self.session.commit()

    def delete(self, project: Project):
        self.session.delete(project)
        self.session.commit()

    # BUG FIX: Implementação - Métodos do repositório para paridade com ConnectionRepository
    def get_active(self):
        # Como tb_projeto não tem campo fl_ativo, todos os projetos são considerados ativos
        return self.get_all()

    def get_by_name(self, nm_projeto: str):
        return (
            self.session
            .query(Project)
            .filter(Project.nm_projeto == nm_projeto)
            .first()
        )

    def exists_by_name(self, nm_projeto: str) -> bool:
        return self.get_by_name(nm_projeto) is not None

    def count(self) -> int:
        return (
            self.session
            .query(Project)
            .count()
        )

    def search(self, text: str):
        return (
            self.session
            .query(Project)
            .filter(Project.nm_projeto.ilike(f"%{text}%"))
            .order_by(Project.nm_projeto)
            .all()
        )

