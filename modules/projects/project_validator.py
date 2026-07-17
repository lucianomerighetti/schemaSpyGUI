# Artefato:  project_validator.py
from __future__ import annotations
from modules.projects.project_dto import ProjectDTO
from core.validation.validator import Validator
from core.validation.validation_report import ValidationReport

from modules.projects.rules.name_rule import NameRule
from modules.projects.rules.database_type_rule import DatabaseTypeRule
from modules.projects.rules.host_rule import HostRule
from modules.projects.rules.schema_rule import SchemaRule
from modules.projects.rules.port_rule import PortRule

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
