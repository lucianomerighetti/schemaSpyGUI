# Artefato:  schema_rule.py
from core.validation.validation_rule import ValidationRule
from core.validation.validation_report import ValidationReport
from typing import Any

class SchemaRule(ValidationRule):
    def validate(self, dto: Any, report: ValidationReport) -> None:
        is_file_db = hasattr(dto, 'is_file_database') and dto.is_file_database
        if not is_file_db:
            if not hasattr(dto, 'nm_schema') or not dto.nm_schema or not dto.nm_schema.strip():
                report.error("nm_schema", "Schema é obrigatório para bancos cliente/servidor.")
