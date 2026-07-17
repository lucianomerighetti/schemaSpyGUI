# Artefato:  port_rule.py
from core.validation.validation_rule import ValidationRule
from core.validation.validation_report import ValidationReport
from typing import Any

class PortRule(ValidationRule):
    def validate(self, dto: Any, report: ValidationReport) -> None:
        is_file_db = hasattr(dto, 'is_file_database') and dto.is_file_database
        if not is_file_db:
            if not hasattr(dto, 'nu_porta') or dto.nu_porta is None or dto.nu_porta <= 0 or dto.nu_porta > 65535:
                report.error("nu_porta", "Porta inválida para bancos cliente/servidor. Deve ser entre 1 e 65535.")
