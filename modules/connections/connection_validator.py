# connection_validator.py


from __future__ import annotations

from modules.connections.connection_dto import ConnectionDTO

from core.validation.validator import Validator
from core.validation.validation_report import ValidationReport

from modules.connections.validators.rules.name_rule import NameRule
from modules.connections.validators.rules.database_type_rule import DatabaseTypeRule
from modules.connections.validators.rules.host_rule import HostRule
from modules.connections.validators.rules.port_rule import PortRule
from modules.connections.validators.rules.database_rule import DatabaseRule
from modules.connections.validators.rules.user_rule import UserRule


class ConnectionValidator(Validator):
    def __init__(self) -> None:
        super().__init__()
        self.configure()

    # Configuração do Pipeline
    def configure(self) -> None:
        (
            self.pipeline
            .add(NameRule())
            .add(DatabaseTypeRule())
            .add(HostRule())
            .add(PortRule())
            .add(DatabaseRule())
            .add(UserRule())
        )

    # Execução
    def validate(self, dto: ConnectionDTO) -> ValidationReport:
        self.reset()
        return self.pipeline.execute(
            dto,
            self.report,
        )