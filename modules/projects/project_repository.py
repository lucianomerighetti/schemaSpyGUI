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
