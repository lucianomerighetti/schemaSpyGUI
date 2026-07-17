# Artefato:  password_rule.py
from core.validation.validation_rule import ValidationRule
from core.validation.validation_report import ValidationReport
from typing import Any

class PasswordRule(ValidationRule):
    def validate(self, dto: Any, report: ValidationReport) -> None:
        is_file_db = hasattr(dto, 'is_file_database') and dto.is_file_database
        if not is_file_db:
            if not hasattr(dto, 'tx_password') or not dto.tx_password or not dto.tx_password.strip():
                report.error("tx_password", "Senha é obrigatória para bancos cliente/servidor.")
