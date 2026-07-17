# Artefato:  name_rule.py
from core.validation.validation_rule import ValidationRule
from core.validation.validation_report import ValidationReport
from typing import Any

class NameRule(ValidationRule):
    def validate(self, dto: Any, report: ValidationReport) -> None:
        if not hasattr(dto, 'nm_projeto') or not dto.nm_projeto or not dto.nm_projeto.strip():
            report.error("nm_projeto", "Nome do projeto é obrigatório.")
