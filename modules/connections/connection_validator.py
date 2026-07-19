# Artefato:  connection_validator.py


from __future__ import annotations

from modules.connections.connection_dto import ConnectionDTO

from core.validation.validator import Validator
from core.validation.validation_report import ValidationReport

# BUG FIX: Alteração - Imports unificados usando a estrutura do __init__.py do pacote rules
from modules.connections.rules import (
    NameRule,
    DatabaseTypeRule,
    HostRule,
    PortRule,
    DatabaseRule,
    UserRule,
    PasswordRule
)


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