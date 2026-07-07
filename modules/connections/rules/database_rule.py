# database_rule.py

from core.validation.validation_rule import ValidationRule
from core.validation.validation_report import ValidationReport
from typing import Any

class DatabaseRule(ValidationRule):
    def validate(self, dto: Any, report: ValidationReport) -> None:
        # BUG FIX Regra vazia anteriormente (apenas comentário). Código antes da correção: (arquivo vazio)
        is_file_db = hasattr(dto, 'is_file_database') and dto.is_file_database
        if is_file_db:
            if not hasattr(dto, 'ds_caminho') or not dto.ds_caminho or not dto.ds_caminho.strip():
                report.error("ds_caminho", "Caminho do arquivo de banco é obrigatório para bancos de arquivo local.")
        else:
            if not hasattr(dto, 'nm_database') or not dto.nm_database or not dto.nm_database.strip():
                report.error("nm_database", "Nome do banco de dados é obrigatório para bancos cliente/servidor.")