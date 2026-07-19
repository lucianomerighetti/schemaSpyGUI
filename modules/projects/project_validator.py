# Artefato:  project_validator.py
from __future__ import annotations
from modules.projects.project_dto import ProjectDTO
from core.validation.validator import Validator
from core.validation.validation_report import ValidationReport

# BUG FIX: Alteração - Imports unificados usando a estrutura do __init__.py do pacote rules
from modules.projects.rules import (
    NameRule,
    DatabaseTypeRule,
    HostRule,
    SchemaRule,
    PortRule
)

class ProjectValidator(Validator):
    def __init__(self) -> None:
        super().__init__()
        self.configure()

    def configure(self) -> None:
        (
            self.pipeline
            .add(NameRule())
            .add(DatabaseTypeRule())
            .add(HostRule())
            .add(SchemaRule())
            .add(PortRule())
        )

    def validate(self, dto: ProjectDTO) -> ValidationReport:
        self.reset()
        return self.pipeline.execute(
            dto,
            self.report,
        )
