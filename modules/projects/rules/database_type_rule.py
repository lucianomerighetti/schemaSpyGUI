# Artefato:  database_type_rule.py
from core.validation.validation_rule import ValidationRule
from core.validation.validation_report import ValidationReport
from typing import Any

class DatabaseTypeRule(ValidationRule):
    def validate(self, dto: Any, report: ValidationReport) -> None:
        if not hasattr(dto, 'tp_database') or not dto.tp_database or not dto.tp_database.strip():
            report.error("tp_database", "Tipo de banco de dados é obrigatório.")
