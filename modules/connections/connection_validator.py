# Artefato:  connection_validator.py


from __future__ import annotations

from modules.connections.connection_dto import ConnectionDTO

from core.validation.validator import Validator
from core.validation.validation_report import ValidationReport

# BUG FIX Caminhos incorretos de importação das regras. Código antes da correção: imports usavam modules.connections.validators.rules
from modules.connections.rules.name_rule import NameRule
from modules.connections.rules.database_type_rule import DatabaseTypeRule
from modules.connections.rules.host_rule import HostRule
from modules.connections.rules.port_rule import PortRule
from modules.connections.rules.database_rule import DatabaseRule
from modules.connections.rules.user_rule import UserRule
from modules.connections.rules.password_rule import PasswordRule


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
            .add(PasswordRule())
        )

    # Execução
    def validate(self, dto: ConnectionDTO) -> ValidationReport:
        self.reset()
        return self.pipeline.execute(
            dto,
            self.report,
        )