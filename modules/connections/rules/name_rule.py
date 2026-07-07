# name_rule.py

from core.validation.validation_rule import ValidationRule
from core.validation.validation_report import ValidationReport
from typing import Any

class NameRule(ValidationRule):
    def validate(self, dto: Any, report: ValidationReport) -> None:
        # BUG FIX Regra vazia anteriormente (apenas comentário). Código antes da correção: (arquivo vazio)
        if not hasattr(dto, 'nm_conexao') or not dto.nm_conexao or not dto.nm_conexao.strip():
            report.error("nm_conexao", "Nome da conexão é obrigatório.")